<?php
session_start();

if($_SESSION['username']=="")
{
	header("Location: ./index.php?message=not-auth");
}
	//The rest of the page.
	echo "Logged in as ".$_SESSION['username'];
	echo "<a href=\"./logout.php\">Logout</a>";



?>