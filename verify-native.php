<?php
$docroot='/usr/local/emhttp';
require_once "$docroot/plugins/dynamix.docker.manager/include/DockerClient.php";
$t=new DockerTemplates();$t->getAllInfo();
$d=json_decode(file_get_contents('/var/local/emhttp/plugins/dynamix.docker.manager/docker.json'),true);
foreach($d as $name=>$v)if(in_array($name,['agent-zero-1','agent-zero-2']))echo json_encode(['name'=>$name,'running'=>$v['running'],'autostart'=>$v['autostart'],'url'=>$v['url'],'template'=>$v['template'],'icon'=>$v['icon']])."\n";
$a=file('/var/lib/docker/unraid-autostart',FILE_IGNORE_NEW_LINES);$b=file('/mnt/fastssd/system/a0-pilot-autostart-before',FILE_IGNORE_NEW_LINES);
echo json_encode(['original_schedule_preserved'=>array_slice($a,0,count($b))===$b,'pilot_entries'=>array_slice($a,count($b))])."\n";
