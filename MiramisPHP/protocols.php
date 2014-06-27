<?php

include "htmlgeneral.php";
include "dbconnect.php";


echo makehead("Протоколы");



#если установлено, вызвать функцию удаления 
if (isset ($_GET['delid'] ))
{
	delitem( $_GET['delid'] );
}


#функция удаляет значение
function delitem ($item)
{

$query = "DELETE FROM `protocols` where id='".$item."'";
$res = mysql_query($query);
	
}


#определить колонки в таблице, по которым будет прозводиться фильтрация по вариантам значения (надо будетпотом добавить по границам)
$varr=array('ProductName'=> 'Название продукта', 'TestName' => 'Название теста' );

 



echo "<h1 align='center'>Протоколы</h1>\n\n";

#функция генерирует див с фильтрами. На входе - словарь имя колонки mysql - название колонки текстом, имя таблицы в mysql
#FEATURE:можно оптимизировать, так как на каждую колонку производится запрос к БД
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
		</select>
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

#производит строку фильтров (WHERE clause), на вход принимает словарь имя колонки mysql - название колонки текстом
function makeFilterString ($vararray)
{
	$fstring="WHERE ";
	foreach ($vararray as $i => $value)
	{
		if (isset($_GET[$i]))
		{
			$val=$_GET[$i];
			if ($val)
			{
				$fstring=$fstring." `".$i."`='".$val."' AND "; 
			}
		}
	}
	if ($fstring=="WHERE ") return "";
	#удалить последнее AND
	$fstring=substr($fstring, 0, -4);
#	echo $fstring;
	return $fstring;
}



#здесь будет формирование строки фильтров 

#обёртка к изготовителю WHERE - если в GET есть Filters, что есть скрытое поле, генерируемое makefilterdiv, то запускать makeFilterSting
function filters()
{
	global $varr;
	if (isset ($_GET['Filters']))
	{
	return makeFilterString($varr);
	}
	return "";

}

#TODO: выделить фильтры и всё, что с ними связно, в отдельный файл PHP


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


echo "<td><a href='../python/FRprotocolViewEdit.py?id=$id'>Правка</a> </td>";
echo "<td><input type='button' onclick=\"destroy('Вы уверенно хотите удалить данный протокол?', 'protocols.php?delid=".$id."' ) \"   value='Удаление'  > </td>";

//href='protocols.php?delid=".$id."'

echo "</tr>";
}

echo "</table>"; 

echo "<a href=''> Создать протокол </a> &nbsp ";

echo "<a href=''> Создать протокол из отчёта</a>  </div>";
 

echo makefoot(); 
?>
