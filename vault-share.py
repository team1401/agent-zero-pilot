"""Move only pilot login items into the established shared Helix collection."""
import ast,pathlib,re,json,sqlite3,subprocess,shlex
P=pathlib.Path(__file__).parent
tree=ast.parse((P/'vault-provision.py').read_text())
remote=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='remote' for t in n.targets)).split('for item in p.get')[0]
remote+='''
org='d43ffb16-4c21-4114-b2b0-b3f201130854'
collection='d33556a6-4f13-43dd-aff8-b3f201130871'
for handle in p['handles']:
 r=run(['/opt/homebrew/bin/bw','get','item',handle['id']],e);before=json.loads(r.stdout)
 assert before['name']==handle['name']
 if not before.get('organizationId'):
  encoded=base64.b64encode(json.dumps([collection]).encode()).decode()
  r=run(['/opt/homebrew/bin/bw','move',handle['id'],org,encoded],e)
  if r.returncode: print(json.dumps({'stage':'share-failed','id':handle['id']}));sys.exit(1)
 r=run(['/opt/homebrew/bin/bw','get','item',handle['id']],e);after=json.loads(r.stdout)
 assert after['organizationId']==org and collection in after['collectionIds']
 assert after['login']==before['login']
 print(json.dumps({'stage':'shared-verified','name':after['name'],'id':after['id'],'organization':'Airstream AI','collection':'Helix'}))
'''
c=sqlite3.connect('/home/helix/.hermes-minimal/state.db')
m=re.fullmatch(r'The password for that is (\S+)\s*',c.execute("select content from messages where id=104372 and role='user'").fetchone()[0],re.I);assert m
handles=[json.loads(l) for l in (P/'vault-handles.jsonl').read_text().splitlines() if l.strip() and json.loads(l).get('stage')=='created-verified']
r=subprocess.run(['ssh','helix@100.117.95.108','/opt/homebrew/bin/python3 -c '+shlex.quote(remote)],input=json.dumps({'keychain_password':m[1],'handles':handles}),capture_output=True,text=True,timeout=240)
print(r.stdout);(P/'vault-shared-handles.jsonl').write_text(r.stdout)
raise SystemExit(r.returncode)
