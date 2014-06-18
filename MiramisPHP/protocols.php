<?php

include "htmlgeneral.php";
include "dbconnect.php";


echo makehead("Протоколы");


if (isset ($_GET['delid'] ))
{
	delitem( $_GET['delid'] );
	
}


$varr=array('ProductName'=> 'Название продукта', 'TestName' => 'имя теста' );

function delitem ($item)
{

$query = "DELETE FROM `protocols` where id='".$item."'";
$res = mysql_query($query);
	
}



#здесь пойдут штуки типа isdel и так далее


#здесь будет формирование строки фильтров 

function filters()
{
 
	if (isset ($_GET['Filters']))
	{
		 
	
	return makeFilterString($varr);
	
	}
	
	
	return "";

}



echo "<h1 align='center'>Протоколы</h1>\n\n";






function makefilterdiv ($vararray, $tablename)
{
echo "
<div id='filters'>
	";
	echo "<b> Фильтры <b>";

	echo "
	<form method='GET' action='protocols.php?Filter=yess'>
		";


foreach ($vararray as $i => $value)
{
	$query="SELECT DISTINCT(`".$i."`)  FROM `".$tablename."`";
	$res = mysql_query($query);
		#echo "Название изделия:";
		echo $vararray[$i];
	 	echo "
		<select name='".$i."' style='width : 200'>
			";
			echo "<option value=''></option>\n   ";
			while ($row=mysql_fetch_array($res))
			{
			echo "<option value='".$row[$i]."'>".$row[$i]."</option>\n";
			}
			echo "
		</select></br>
		";
}
		echo "</br>
		<input type ='submit' value='Применить'>
		<input type='hidden' name='Filters' value='yess'>
		";
		echo"
	</form>
</div>\n\n";

}


function makeFilterString ($vararray)
{
		 
		 
	$fstring="WHERE ";
/* 	
	foreach ($vararray as $i => $value)
	{
		if (isset($_GET($i)))
		{
			$val=$_GET($i);
			if ($val)
			{
				$fstring=$fstring." ".$i."=".$val." AND "; 
			
			}
			
		}
 		
		
	}
  
 
 */
	#удалить последнее AND
	
	$fstring=substr($fstring, 0, -4);

	echo ($fstring);
	
	return $fstring;
	
	
	
}



#здесь выводятся фильтры


echo makefilterdiv($varr, 'protocols');




$query = "SELECT * FROM `protocols` ".filters();
$res = mysql_query($query);


echo "<div align='left'> <table class='itemstable'>";

while($row = mysql_fetch_array($res))
{
	
$id=$row['ID'];
	
echo "<tr>";
echo "<td>".$id."</td>\n";

echo "<td>".$row['ProductName']."</td>\n";
echo "<td>".$row['TestName']."</td>\n";


echo "<td><a href=''>Правка</a> </td>";
echo "<td><input type='button' onclick=\"destroy('Вы уверенно хотите удалить данный протокол?', 'protocols.php?delid=".$id."' ) \"   value='Удаление'  > </td>";

//href='protocols.php?delid=".$id."'

echo "</tr>";
}

echo "</table>"; 

echo "<a href=''> Создать протокол </a>  </div>";
 

echo makefoot(); 
?>
