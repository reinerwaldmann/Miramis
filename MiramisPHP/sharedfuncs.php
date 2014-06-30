<?php
function makefilterdiv ($vararray, $tablename, $action)
#функция генерирует див с фильтрами. На входе - словарь имя колонки mysql - название колонки текстом, имя таблицы в mysql
#FEATURE:можно оптимизировать, так как на каждую колонку производится запрос к БД

{
echo "
<div id='filters'>
	";
	echo "<b> Фильтры <b>";

	echo "
	<form method='GET' action='$action'>
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
		</select> </br>
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
?>