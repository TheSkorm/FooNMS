<?php

function redirectIfNotLoggedIn()
{
	//Send an HTTP header to redirect to the login page if there is no username in the session variable.
	if($_SESSION['username']=="")
	{
		header("Location: ./index.php?message=not-auth");

		//Don't do anything else, just die.
		exit();
	}

	
}

?>