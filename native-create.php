<?php
$docroot='/usr/local/emhttp';
$driver=['bridge'=>'bridge','host'=>'host','none'=>'none'];
$subnet=['bridge'=>'172.17.0.0/16'];
$ident=parse_ini_file('/boot/config/ident.cfg');
$var=['timeZone'=>'America/Los_Angeles','NAME'=>$ident['NAME']];
require_once "$docroot/plugins/dynamix.docker.manager/include/Helpers.php";
$before=file_get_contents('/var/lib/docker/unraid-autostart');
file_put_contents('/mnt/fastssd/system/a0-pilot-autostart-before',$before);
foreach ([1,2] as $i) {
 $name="agent-zero-$i";
 $path="/boot/config/plugins/dockerMan/templates-user/my-$name.xml";
 [$cmd,$actual,$image]=xmlToCommand($path,true);
 if ($actual!==$name || strpos($cmd,'--privileged')!==false || strpos($cmd,'100.108.186.69:'.(50079+$i).':80')===false) throw new Exception('unsafe command');
 exec($cmd.' 2>&1',$out,$rc); if($rc)throw new Exception(implode("\n",$out));
 echo "$name created natively\n";
 exec('docker start '.escapeshellarg($name).' 2>&1',$start,$rc);if($rc)throw new Exception('start failed');
 echo "$name started\n";
}
$after=file_get_contents('/var/lib/docker/unraid-autostart');
if($after!==$before)throw new Exception('concurrent autostart change');
file_put_contents('/var/lib/docker/unraid-autostart',rtrim($before)."\nagent-zero-1 0\nagent-zero-2 0\n");
require_once "$docroot/plugins/dynamix.docker.manager/include/DockerClient.php";
$t=new DockerTemplates();$t->getAllInfo();
echo "Native cache refreshed\n";
