"""Authorized Mac Keychain unlock and Bitwarden provisioning. No secret stdout."""
import json, sqlite3, re, subprocess, base64, pathlib, os
ROOT=pathlib.Path(__file__).parent
c=sqlite3.connect('/home/helix/.hermes-minimal/state.db')
t=c.execute("select content from messages where id=104372 and session_id='20260921_065527_ebd12a' and role='user'").fetchone()[0]
m=re.fullmatch(r'The password for that is (\S+)\s*',t,re.I)
assert m, 'Explicit authorized keychain credential not found'
payload={'keychain_password':m[1]}
private=ROOT/'.credentials.json'
if private.exists(): payload['items']=json.loads(private.read_text())
remote='''import sys,json,subprocess,os,base64
p=json.load(sys.stdin)
k='/Users/helix/Library/Keychains/login.keychain-db'
def run(args,env=None):
 return subprocess.run(args,env=env,capture_output=True,text=True,stdin=subprocess.DEVNULL,timeout=90)
r=run(['security','unlock-keychain','-p',p['keychain_password'],k])
if r.returncode: print(json.dumps({'stage':'keychain-unlock','ok':False,'code':r.returncode}));sys.exit(1)
r=run(['security','find-generic-password','-w','-a','helix','-s','HERMES_BITWARDEN_MASTER_PASSWORD',k])
if r.returncode: print(json.dumps({'stage':'master-reference','ok':False,'code':r.returncode}));sys.exit(1)
e=os.environ.copy();e['BW_PASSWORD']=r.stdout.strip()
r=run(['/opt/homebrew/bin/bw','unlock','--passwordenv','BW_PASSWORD','--raw'],e)
if r.returncode or not r.stdout.strip() or '\\n' in r.stdout.strip(): print(json.dumps({'stage':'vault-unlock','ok':False,'code':r.returncode}));sys.exit(1)
e['BW_SESSION']=r.stdout.strip();e.pop('BW_PASSWORD',None)
s=run(['/opt/homebrew/bin/bw','status'],e)
status=json.loads(s.stdout);print(json.dumps({'stage':'vault','status':status.get('status')}))
for item in p.get('items',[]):
 obj={'type':1,'name':item['name'],'notes':'Agent Zero pilot on Strix. Tailscale-only native Unraid container.','login':{'username':item['username'],'password':item['password'],'uris':[{'match':0,'uri':item['url']}]}}
 r=run(['/opt/homebrew/bin/bw','create','item',base64.b64encode(json.dumps(obj).encode()).decode()],e)
 try: created=json.loads(r.stdout); ident=created['id']
 except Exception: print(json.dumps({'stage':'create','name':item['name'],'ok':False}));sys.exit(1)
 r=run(['/opt/homebrew/bin/bw','get','item',ident],e);v=json.loads(r.stdout)
 assert v['login']['password']==item['password'] and v['login']['username']==item['username']
 print(json.dumps({'stage':'created-verified','name':item['name'],'id':ident}))
'''
r=subprocess.run(['ssh','-o','BatchMode=yes','helix@100.117.95.108', '/opt/homebrew/bin/python3 -c '+__import__('shlex').quote(remote)],input=json.dumps(payload),capture_output=True,text=True,timeout=240)
print(r.stdout)
if r.returncode: print('Remote credential provisioning failed; exit',r.returncode)
raise SystemExit(r.returncode)
