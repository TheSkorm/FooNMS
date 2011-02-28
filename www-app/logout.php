<?php
require_once("includes/user-management.inc");

session_start();

unset($_SESSION['username']);

header("Location: ./index.php?message=logout");

?>
