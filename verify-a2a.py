import sys,json,requests,subprocess,uuid,shlex,time
from pilot_client import Client,P
results=[]
for i in (1,2):
 c=Client(i);c.api('settings_set',{'settings':{'a2a_server_enabled':True}})
 s=c.api('settings_get')['settings'];assert s['a2a_server_enabled'] is True
 token=s['mcp_server_token'];assert token and token!='********'
 url=c.url+'/a2a/t-'+token
 bad=requests.get(c.url+'/a2a/t-invalid/.well-known/agent.json',timeout=15)
 card=requests.get(url+'/.well-known/agent.json',timeout=30)
 print(i,'invalid-token',bad.status_code,'valid-token-card',card.status_code)
 results.append({'instance':i,'enabled':True,'invalid_token_status':bad.status_code,'valid_card_status':card.status_code})
 if card.status_code==200:
  obj=card.json();print('card',obj.get('name'),'capabilities',obj.get('capabilities'))
 if i==2:
  script='''import json,sys,requests,time
p=json.load(sys.stdin)
r=requests.post(p['url']+'/',json=p['body'],timeout=240)
try: body=r.json()
except ValueError: body={'non_json':r.text[:500]}
print(json.dumps({'status':r.status_code,'body':body}))
'''
  body={'jsonrpc':'2.0','id':str(uuid.uuid4()),'method':'message/send','params':{'message':{'kind':'message','role':'user','parts':[{'kind':'text','text':'Controlled one-shot A2A connectivity test from the other pilot container. Reply with exactly A2A_LOCAL_OK. Do not call tools, delegate, change files, or send any further messages.'}],'messageId':str(uuid.uuid4())}}}
  cmd=['ssh','root@<agent-zero-host>','docker exec -i agent-zero-1 /opt/venv-a0/bin/python -c '+shlex.quote(script)]
  r=subprocess.run(cmd,input=json.dumps({'url':url,'body':body}),capture_output=True,text=True,timeout=270)
  print('exchange',r.returncode,r.stdout[:10000],r.stderr.replace(token,'[REDACTED]')[:1800]);results[-1]['exchange']=json.loads(r.stdout) if r.stdout.strip() else {'error':r.returncode}
(P/'a2a-verification.json').write_text(json.dumps(results,indent=2))
