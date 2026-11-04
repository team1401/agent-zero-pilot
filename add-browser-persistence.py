import subprocess,pathlib,xml.etree.ElementTree as ET,json
from pilot_client import Client,P
# Only the two newly installed pilot containers; no original app lifecycle changes.
for i in (1,2):
 c=Client(i);r=c.api('poll');assert not any(x['running'] for x in r.get('contexts',[]))
 c.api('plugins/_desktop/desktop_session',{'action':'shutdown','save_first':True})
 name=f'agent-zero-{i}'
 path=P/f'my-{name}.xml';root=ET.parse(path).getroot()
 ET.SubElement(root,'Config',{'Name':'Persistent browser profile','Target':'/a0/tmp/browser','Default':f'/mnt/fastssd/AppData/{name}/browser','Mode':'rw','Type':'Path','Display':'always','Required':'true','Mask':'false'}).text=f'/mnt/fastssd/AppData/{name}/browser'
 for key in ['HF_HUB_OFFLINE','TRANSFORMERS_OFFLINE']:
  ET.SubElement(root,'Config',{'Name':key,'Target':key,'Default':'1','Type':'Variable','Display':'advanced','Required':'true','Mask':'false'}).text='1'
 # umask protects regenerated dotenv/settings files too.
 root.find('ExtraParams').text+=' --entrypoint=/bin/sh'
 root.find('PostArgs').text='-c "umask 077; exec /exe/initialize.sh main"'
 ET.ElementTree(root).write(path,encoding='utf-8',xml_declaration=True)
 subprocess.run(['ssh','root@<agent-zero-host>',f'docker stop {name} && test ! -e /mnt/fastssd/AppData/{name}/browser && docker cp {name}:/a0/tmp/browser /mnt/fastssd/AppData/{name}/browser && chmod 700 /mnt/fastssd/AppData/{name}/browser'],check=True)
 subprocess.run(['scp','-q',str(path),'root@<agent-zero-host>:/boot/config/plugins/dockerMan/templates-user/'],check=True)
subprocess.run(['scp','-q',str(P/'native-recreate.php'),'root@<agent-zero-host>:/mnt/fastssd/system/a0-native-recreate.php'],check=True)
r=subprocess.run(['ssh','root@<agent-zero-host>','php /mnt/fastssd/system/a0-native-recreate.php && docker start agent-zero-1 agent-zero-2'],capture_output=True,text=True,check=True)
print(r.stdout[-2000:]);print('Both pilots recreated through native Docker Manager with isolated browser persistence.')
