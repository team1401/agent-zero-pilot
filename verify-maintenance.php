<?php
$b='/mnt/fastssd/system/agent-zero-maintenance-20261021-151300';
$before=json_decode(file_get_contents("$b/inspect-before.json"),true);
$after=json_decode(shell_exec('docker inspect $(docker ps -aq)'),true);$map=[];foreach($after as $v)$map[$v['Name']]=$v;
foreach($before as $v){$a=$map[$v['Name']]??[];usort($v['Mounts'],fn($x,$y)=>strcmp($x['Destination'],$y['Destination']));usort($a['Mounts'],fn($x,$y)=>strcmp($x['Destination'],$y['Destination']));echo json_encode(['name'=>$v['Name'],'previous_running'=>$v['State']['Running'],'running'=>$a['State']['Running']??false,'same_id'=>$v['Id']===($a['Id']??''),'same_policy'=>$v['HostConfig']['RestartPolicy']===($a['HostConfig']['RestartPolicy']??null),'same_mounts'=>$v['Mounts']==($a['Mounts']??null),'native_label'=>$a['Config']['Labels']['net.unraid.docker.managed']??null,'health'=>$a['State']['Health']['Status']??null])."\n";}
echo 'autostart_unchanged='.(hash_file('sha256',"$b/unraid-autostart")===hash_file('sha256','/var/lib/docker/unraid-autostart')?'yes':'NO')."\n";
echo 'guard_restored='.(file_exists('/boot/config/plugins/qbit-dependency-guard/disabled')?'NO':'yes')."\n";
$c=json_decode(file_get_contents('/mnt/fastssd/AppData/qbittorrent/admin-credentials.json'),true);
$h=curl_init();curl_setopt_array($h,[CURLOPT_RETURNTRANSFER=>true,CURLOPT_TIMEOUT=>15,CURLOPT_COOKIEFILE=>'']);
function api($p,$data=null){global $h;curl_setopt($h,CURLOPT_URL,'http://192.168.1.40:8080/api/v2/'.$p);curl_setopt($h,CURLOPT_POST,$data!==null);if($data!==null)curl_setopt($h,CURLOPT_POSTFIELDS,http_build_query($data));$r=curl_exec($h);return [curl_getinfo($h,CURLINFO_HTTP_CODE),$r];}
$l=api('auth/login',$c);$p=api('app/preferences');$t=api('torrents/info');$v=json_decode($p[1],true);$ts=json_decode($t[1],true);
echo json_encode(['qbit_login_http'=>$l[0],'authenticated_preferences'=>$p[0]===200&&isset($v['listen_port']),'torrent_count'=>is_array($ts)?count($ts):null,'listen_port'=>$v['listen_port']??null,'forwarded_port_matches'=>trim(file_get_contents('/mnt/fastssd/AppData/gluetun/forwarded_port'))==($v['listen_port']??null),'interface'=>$v['current_network_interface']??null])."\n";
foreach(['proton-vpn','qbittorrent'] as $name){$pid=$map['/'.$name]['State']['Pid'];echo "$name netns=".readlink("/proc/$pid/ns/net")."\n";}
$docroot='/usr/local/emhttp';require_once "$docroot/plugins/dynamix.docker.manager/include/DockerClient.php";$d=new DockerTemplates();$d->getAllInfo();echo "native_cache_refreshed=yes\n";
