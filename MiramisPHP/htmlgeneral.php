<?php


function makehead($pagename)
{
	echo "<html lang='ru' >\n";
	echo "<head>\n";
	echo "<title>".$pagename."</title>\n";
	echo "<meta charset=\"utf-8\">\n";
	echo "<link rel='stylesheet' type='text/css' href='main.css'>"; #ссылка на ксску
	echo "<script type='text/javascript' src='scripts.js'></script>";


	echo "</head>\n";
	echo "<body>\n";

	echo "<a href='protocols.php'> Обзор протоколов </a> &nbsp&nbsp&nbsp&nbsp <a href='results.php'> Обзор результатов </a>";
	
		
}



function makefoot()
{
	
	echo "\n\n</body>\n</html>";
	
}






?>





