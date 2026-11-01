import json, requests, pathlib
P=pathlib.Path(__file__).parent
class Client:
 def __init__(self,i):
  self.i=i;self.credential=json.loads((P/'.credentials.json').read_text())[i-1];self.url=self.credential['url'];self.s=requests.Session()
  r=self.s.post(self.url+'/login',data={'username':self.credential['username'],'password':self.credential['password']},timeout=15);r.raise_for_status()
  token=self.s.get(self.url+'/api/csrf_token',timeout=15).json();assert token['ok'];self.s.headers['X-CSRF-Token']=token['token'];self.s.headers['Origin']=self.url
 def api(self,path,data=None,timeout=120):
  r=self.s.post(self.url+'/api/'+path,json=data or {},timeout=timeout);r.raise_for_status();return r.json()
 def save(self,name,data): (P/f'{name}-{self.i}.json').write_text(json.dumps(data,indent=2))
if __name__=='__main__':
 for i in (1,2):
  c=Client(i);r=c.api('plugins/_desktop/desktop_session',{'action':'desktop'},timeout=180);c.save('desktop-start',r);print('desktop',i,json.dumps(r))
  r=c.api('message_async',{'text':f'Pilot verification instance {i}. Use your code execution tool to create /a0/usr/workdir/pilot-instance-{i}.txt containing exactly INSTANCE_{i}_AGENT_CREATED. Read it back with the tool. Then use your browser to open https://example.com and report its page title. Do not access host files, change settings, use cloud models, or install anything. Finish after reporting both results.'});c.save('task-start',r);print('task',i,r)
