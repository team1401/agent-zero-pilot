import json, pathlib, secrets, os, xml.etree.ElementTree as ET, subprocess
P=pathlib.Path(__file__).parent
os.umask(0o077)
creds=P/'.credentials.json'
assert not creds.exists(), 'Do not rotate existing pilot credentials'
items=[{'name':f'Strix Agent Zero {i}','username':'brian','password':secrets.token_urlsafe(32),'url':f'http://<agent-zero-host>:{50079+i}'} for i in (1,2)]
creds.write_text(json.dumps(items));creds.chmod(0o600)
for i,item in enumerate(items,1):
 name=f'agent-zero-{i}'; stage=P/f'stage-{i}';stage.mkdir();usr=stage/'usr';(usr/'plugins/_model_config').mkdir(parents=True)
 (usr/'.env').write_text(f'AUTH_LOGIN={item["username"]}\nAUTH_PASSWORD={item["password"]}\n')
 (usr/'.env').chmod(0o600)
 # One local preset only, no cloud fallbacks. Text-only model is not misrepresented as vision.
 model={'provider':'lm_studio','name':'halogen-qwen3.8-flash-next','api_base':'http://<agent-zero-host>:8731/v1','ctx_length':32768,'kwargs':{'temperature':0.2,'max_tokens':4096},'rl_requests':0,'rl_input':0,'rl_output':0}
 preset={'name':'Default','chat':dict(model,ctx_history=0.7,vision=False),'utility':dict(model,ctx_input=0.7),'embedding':{'provider':'huggingface','name':'sentence-transformers/all-MiniLM-L6-v2','api_base':'','kwargs':{'model_kwargs':{'local_files_only':True}}}}
 (usr/'plugins/_model_config/presets.yaml').write_text(json.dumps([preset],indent=2))
 root=ET.parse(P/'upstream-ca-template.xml').getroot()
 for k,v in {'Name':name,'WebUI':item['url'],'ExtraParams':f'--memory=8g --cpus=4 --shm-size=1g -p <agent-zero-host>:{50079+i}:80','PostArgs':'','Requires':'','Overview':'Two-instance local-only Agent Zero pilot; CA Selfhosters derived. Authentication in protected persistent usr/.env. No GPU passthrough or host access.'}.items(): root.find(k).text=v
 for elem in list(root.findall('Config')):root.remove(elem)
 ET.SubElement(root,'Config',{'Name':'Persistent user data','Target':'/a0/usr','Default':f'/mnt/fastssd/AppData/{name}/usr','Mode':'rw','Type':'Path','Display':'always','Required':'true','Mask':'false'}).text=f'/mnt/fastssd/AppData/{name}/usr'
 ET.SubElement(root,'TailscaleEnabled').text=''
 ET.ElementTree(root).write(P/f'my-{name}.xml',encoding='utf-8',xml_declaration=True)
 subprocess.run(['ssh','root@<agent-zero-host>',f'test ! -e /mnt/fastssd/AppData/{name} && mkdir -m 700 /mnt/fastssd/AppData/{name}'],check=True)
 subprocess.run(['scp','-qr',str(usr),f'root@<agent-zero-host>:/mnt/fastssd/AppData/{name}/'],check=True)
 subprocess.run(['scp','-q',str(P/f'my-{name}.xml'),'root@<agent-zero-host>:/boot/config/plugins/dockerMan/templates-user/'],check=True)
 print(name,'protected data and native CA template staged')
