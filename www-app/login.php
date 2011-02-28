<?php
require_once("includes/user-management.inc");
require_once("config.inc");

session_start();

$username = htmlspecialchars($_POST["username"]);
$password = sha1(htmlspecialchars($_POST["password"]));

echo $username." ".$password;

$db_connection = mysqli_connect($FOONMS_DATABASE_SERVER,$FOONMS_DATABASE_USERNAME,$FOONMS_DATABASE_PASSWORD);
mysqli_select_db($db_connection,$FOONMS_DATABASE_DBNAME);
$q = mysqli_query($db_connection,"SELECT * FROM users WHERE username = '".$username."';");

if($abc = mysqli_fetch_row($q))
{
	//Username exists. Password not checked.

	$dbusername = $abc[0];
	$dbemail = $abc[1];
	$dbpassword = $abc[2];

	if($password == $dbpassword)
	{
		//Start a new session.
		$_SESSION['username'] = $username;

		//Redirect to the home page.
		header("Location: ./home.php");

	} else {
		//Go back to index.php with an error message.
		header("Location: ./index.php?message=auth-fail");
	}
} else {
	//Username does not exist.
	header("Location: ./index.php?message=auth-fail");
}
?>
