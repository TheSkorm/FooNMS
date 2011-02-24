<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<title>FooNMS - Login</title>

	<meta http-equiv="content-type" content="text/html;charset=ISO-8859-1" />

        <!--
	Because I *really* hate it when people do cool CSS tricks on websites and never reveal them, let me share the link-love:
	http://www.wpdfd.com/editorial/thebox/deadcentre3.html
	-->
	<style type="text/css" media="screen">
		body 
		{
			color: #FFFFFF;
			background-color: #FFFFFF;
			margin: 0px
		}

		#horizon        
		{
			color: #000000;
			background-color: transparent;
			text-align: center;
			position: absolute;
			top: 50%;
			left: 0px;
			width: 100%;
			height: 1px;
			overflow: visible;
			visibility: visible;
			display: block
		}

		#content    
		{
			font-family: Verdana, Geneva, Arial, sans-serif;
			background-color: transparent;
			margin-left: -200px;
			position: absolute;
			top: -140px;
			left: 50%;
			width: 400px;
			height: 280px;
			visibility: visible
		}

		.bodytext 
		{
			font-size: 14px
		}

		.headline 
		{
			font-weight: bold;
			font-size: 24px
		}

		#footer 
		{
			font-size: 11px;
			font-family: Verdana, Geneva, Arial, sans-serif;
			text-align: center;
			position: absolute;
			bottom: 0px;
			left: 0px;
			width: 100%;
			height: 30px;
			visibility: visible;
			display: block;
			color: #000000
		}

		a:link, a:visited 
		{
			color: #0040FF;
			text-decoration: none;
			font-weight: bold;
		}
	</style>
</head>
<body>
	<div id="horizon">

		<div id="content">
			<div class="bodytext">
				<!--<span class="headline">FooNMS</span><br />-->
                            <img alt="FooNMS Logo"  src="./logo-large.png" />
				<form id="input" action="login.php" method="post">
					Username: <input type="text" name="username" /><br />
					Password: <input type="password" name="password" /><br />
					<input type="submit" name="submit" value="Submit" />
				</form>
                            <?php
				
                                if(htmlspecialchars($_GET["message"])=="auth-fail")
                                {
                                    echo "Authentication failed. Try again.";
                                }
				if(htmlspecialchars($_GET["message"])=="logout")
                                {
                                    echo "Successfully logged out.";
                                }
				if(htmlspecialchars($_GET["message"])=="not-auth")
                                {
                                    echo "Not authorised.";
                                }
                            ?>
			</div>
		</div>
	</div>
	
	<div id="footer">
		Copyright &copy; 2010-2011 The Foo Project.
	</div>
</body>
</html>

