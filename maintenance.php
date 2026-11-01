<?php
// Native Docker settings apply; private backups never emitted.
$base='/mnt/fastssd/system/agent-zero-maintenance-'.gmdate('Ymd-His');
umask(0077); mkdir($base,0700,true);
function run($c){exec($c.' 2>&1',$o,$r);if($r)throw new Exception("Command failed: $c ($r)");return implode("\n",$o);}
$cfg='/boot/config/docker.cfg';$orig=file_get_contents($cfg);
if(!str_contains($orig,'DOCKER_IMAGE_SIZE="30"')||!str_contains($orig,'/mnt/fastssd/system/docker/docker.img'))throw new Exception('Unexpected configuration');
if(disk_free_space('/mnt/fastssd/system/docker')<100*1024**3)throw new Exception('Insufficient backing capacity');
$guard='/boot/config/plugins/qbit-dependency-guard/disabled';$hadGuard=file_exists($guard);
copy($cfg,"$base/docker.cfg");
run('tar -czf '.escapeshellarg("$base/configs.tgz").' /boot/config/plugins/dockerMan/templates-user /boot/config/plugins/qbit-dependency-guard /boot/config/plugins/dynamix/qbit-dependency-guard.cron /boot/config/qbit-port-sync.php /var/lib/docker/unraid-autostart /mnt/fastssd/AppData/qbittorrent/admin-credentials.json /mnt/fastssd/AppData/qbittorrent/config/qBittorrent/qBittorrent.conf');
copy('/var/log/docker.log',"$base/docker-before.log");
$inventory=json_decode(run('docker inspect $(docker ps -aq)'),true);file_put_contents("$base/inspect-before.json",json_encode($inventory));
$running=array_values(array_map(fn($x)=>ltrim($x['Name'],'/'),array_filter($inventory,fn($x)=>$x['State']['Running'])));
file_put_contents("$base/running.json",json_encode($running));
copy('/var/lib/docker/unraid-autostart',"$base/unraid-autostart");
echo "BACKUP=$base\nRUNNING=".implode(',',$running)."\n";
file_put_contents($guard,"Approved Docker maintenance\n");
$lock=fopen('/var/run/qbit-dependency-guard/guard.lock','c');flock($lock,LOCK_EX);
try {
 file_put_contents($cfg,str_replace('DOCKER_ENABLED="yes"','DOCKER_ENABLED="no"',$orig));
 echo 'STOP_REQUEST='.gmdate('c')."\n";
 run("/usr/local/sbin/emcmd 'cmdStatus=Apply'");
 for($i=0;$i<120;$i++){exec('mountpoint -q /var/lib/docker',$z,$r);if($r!==0)break;sleep(2);}
 if($r===0)throw new Exception('Native stop did not unmount image');
 echo 'STOPPED='.gmdate('c')."\n";
 $new=str_replace('DOCKER_IMAGE_SIZE="30"','DOCKER_IMAGE_SIZE="80"',$orig);
 file_put_contents($cfg,$new);
 run("/usr/local/sbin/emcmd 'cmdStatus=Apply'");
 for($i=0;$i<120;$i++){exec('docker info >/dev/null 2>&1',$z,$r);if($r===0)break;sleep(2);}
 if($r!==0)throw new Exception('Native restart failed');
 echo 'DAEMON_UP='.gmdate('c')."\n";
 sleep(25);
 foreach($running as $n){if($n==='qbittorrent')continue;run('docker start '.escapeshellarg($n));}
 for($i=0;$i<90;$i++){if(trim(run("docker inspect -f '{{.State.Health.Status}}' proton-vpn"))==='healthy')break;sleep(2);}
 echo 'VPN='.trim(run("docker inspect -f '{{.State.Health.Status}}' proton-vpn"))."\n";
 // Container IDs are retained across service restart. Native repair only if needed later.
 exec('docker start qbittorrent 2>&1',$q,$qr);echo 'QBIT_START_RC='.$qr."\n";
 echo run('df -hT /var/lib/docker /mnt/fastssd/system/docker/docker.img')."\n";
 echo run("docker ps --format '{{.Names}} {{.Status}}'")."\n";
 file_put_contents("$base/inspect-after.json",run('docker inspect $(docker ps -aq)'));
 echo 'END='.gmdate('c')."\n";
} finally {
 // Never intentionally leave Docker disabled after an interrupted maintenance.
 $now=file_get_contents($cfg);if(str_contains($now,'DOCKER_ENABLED="no"')){file_put_contents($cfg,str_replace('DOCKER_ENABLED="no"','DOCKER_ENABLED="yes"',$now));exec("/usr/local/sbin/emcmd 'cmdStatus=Apply'");}
 if(!$hadGuard)unlink($guard);flock($lock,LOCK_UN);
}
