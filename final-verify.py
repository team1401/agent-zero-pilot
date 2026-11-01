import subprocess,json,pathlib,requests,sys,time
from pilot_client import Client,P
r=json.loads((P/'a2a-verification.json').read_text());tid=r[1]['exchange']['body']['result']['id'];c=Client(2);token=c.api('settings_get')['settings']['mcp_server_token'];url=c.url+'/a2a/t-'+token+'/'
for n in range(60):
 x=requests.post(url,json={'jsonrpc':'2.0','id':'pilot-poll','method':'tasks/get','params':{'id':tid}},timeout=20);d=x.json();state=d.get('result',{}).get('status',{}).get('state')
 if state in ['completed','failed','canceled','rejected']:break
 time.sleep(3)
(P/'a2a-task-final.json').write_text(json.dumps(d,indent=2));print('A2A',state,json.dumps(d)[:7000])
raw=subprocess.check_output(['ssh','root@100.108.186.69','docker inspect $(docker ps -aq)']).decode();items=json.loads(raw)
summary=[]
for x in items:
 name=x['Name'].lstrip('/');item={'name':name,'id':x['Id'],'status':x['State']['Status'],'started_at':x['State']['StartedAt']}
 if name.startswith('agent-zero-'):
  item.update({'image':x['Image'],'ports':x['HostConfig']['PortBindings'],'privileged':x['HostConfig']['Privileged'],'network':x['HostConfig']['NetworkMode'],'memory':x['HostConfig']['Memory'],'cpus':x['HostConfig']['NanoCpus'],'mounts':x['Mounts'],'labels':x['Config']['Labels']})
 summary.append(item)
(P/'deployment-inventory.json').write_text(json.dumps(summary,indent=2));print('running',sum(x['status']=='running' for x in summary),'stopped',sum(x['status']!='running' for x in summary))
for i in (1,2):
 c=Client(i);ctx=json.loads((P/f'task-start-{i}.json').read_text())['context'];poll=c.api('poll',{'context':ctx});c.save('final-chat',poll)
 a=subprocess.check_output(['ssh','root@100.108.186.69',f"docker exec agent-zero-{i} sh -c 'test ! -e /a0/usr/workdir/pilot-instance-{3-i}.txt && echo ISOLATED; stat -c %a /a0/usr/.env; cd /a0 && git describe --tags --always'"]).decode();print('instance',i,a)
 s=c.api('settings_get')['settings'];print('auth-config',bool(s.get('auth_login')), 'a2a-enabled',s['a2a_server_enabled'],'mcp-disabled',not s['mcp_server_enabled'])
 c.save('safe-settings',{'a2a_server_enabled':s['a2a_server_enabled'],'mcp_server_enabled':s['mcp_server_enabled'],'auth_configured':bool(s.get('auth_login'))})
