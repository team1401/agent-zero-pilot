<?php
$docroot='/usr/local/emhttp';chdir($docroot);
$_SERVER['DOCUMENT_ROOT']=$docroot;
$_SERVER['REQUEST_URI']='/plugins/dynamix.docker.manager/include/CreateDocker.php';
$_GET=['updateContainer'=>1,'mute'=>1,'ct'=>['agent-zero-1','agent-zero-2']];
$_POST=[];
require "$docroot/plugins/dynamix.docker.manager/include/CreateDocker.php";
