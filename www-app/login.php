<?php
session_start();

$username = htmlspecialchars($_POST["username"]);
$password = sha1(htmlspecialchars($_POST["password"]));

echo $username." ".$password;

$db_connection = mysqli_connect("localhost","foonms","foonms");

$rowcount = 0;

mysqli_select_db($db_connection,"foonms");
$q = mysqli_query($db_connection,"select * from users where username = '".$username."';");

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
