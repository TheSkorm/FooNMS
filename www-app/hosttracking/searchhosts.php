<?
require_once("../includes/user-management.inc");
require_once("../config.inc");
error_reporting(E_ERROR | E_WARNING | E_PARSE | E_NOTICE);

/* 
convert the IP address from a dotted decimal to a long unsigned  in string form
if the ip address is empty find everything*/
$ip = sprintf('%u',ip2long($_GET['ip']));
if (!$ip){
$ip='%%';
}

$switch = sprintf('%u',ip2long($_GET['switch']));
if (!$switch){
$switch='%%';
}

$router = sprintf('%u',ip2long($_GET['router']));
if (!$router){
$router='%%';
}

$db_connection = mysqli_connect($FOONMS_DATABASE_SERVER,$FOONMS_DATABASE_USERNAME,$FOONMS_DATABASE_PASSWORD);
mysqli_select_db($db_connection,$FOONMS_DATABASE_DBNAME) or die("incorrect database details");
$q = mysqli_query($db_connection,"SELECT * FROM arps LEFT OUTER JOIN macs ON (arps.macaddress=macs.macaddress)
where ipaddress like '".$ip."'
and switch like '".$switch."'
and router like '".$router."'
and hostname like '%".mysqli_real_escape_string($db_connection,$_GET['hostname'])."%'
and arps.macaddress like '%".mysqli_real_escape_string($db_connection,$_GET['mac'])."%'
and portname like '%".mysqli_real_escape_string($db_connection,$_GET['port'])."'
") or die("query error");


while($row = mysqli_fetch_array($q)){
print "IP Address :" . long2ip($row["ipaddress"]) . "<br>";
print "Hostname :" . $row["hostname"] . "<br>";
print "MAC Address :" . $row["macaddress"] . "<br>";
print "Switch :" . long2ip($row["switch"]) . "<br>";
print "Port :" . $row["portname"] . "<br>";
print "Router :" . long2ip($row["router"]) . "<br>";
print "Time :" . $row["time"] . "<br>";


echo "<br>";

}
print ip2long($_GET['ip']);

?>
