<?php


include "htmlgeneral.php";
include "dbconnect.php";
include "sharedfuncs.php";




echo makehead("Результаты");



#если установлено, вызвать функцию удаления
if (isset ($_GET['delid'] ))
{
	delitem( $_GET['delid'] );
}


#функция удаляет значение
function delitem ($item)
{

$query = "DELETE FROM `results` where id='".$item."'";
$res = mysql_query($query);

}

//определить колонки в таблице, по которым будет прозводиться фильтрация по вариантам значения (надо будетпотом добавить по границам)
$varr=array('ProductName'=> 'Название продукта', 'TestName' => 'Название теста', 'Operator' =>'Оператор', 'Date' => 'Дата',
'SerialNumber'=> 'Номер серийный', 'BatchNumber' => 'Номер партии');

echo "<h1 align='center'>Результаты</h1>\n\n";


#здесь выводятся фильтры

echo makefilterdiv($varr, 'results', "results.php?Filter=yess");


$query = "SELECT * FROM `results` ".filters();

$res = mysql_query($query);


echo "<div align='left'> <table class='itemstable'>";
echo "<tr>";
echo "<td><b>ID</b></td>";
echo "<td><b>Название изделия</b></td>";
echo "<td><b>Название испытания</b></td>";
echo "<td><b>Оператор</b></td>";
echo "<td><b>Дата</b></td>";
echo "<td><b>Серийный номер</b></td>";
echo "<td><b>Номер партии</b></td>";
echo "<td></td>";
echo "<td></td>";

echo "</tr>";



while($row = mysql_fetch_array($res))
{

$id=$row['ID'];
echo "<tr>";
echo "<td>".$id."</td>\n";
echo "<td>".$row['ProductName']."</td>\n";
echo "<td>".$row['TestName']."</td>\n";
echo "<td>".$row['Operator']."</td>\n";
echo "<td>".$row['Date']."</td>\n";
echo "<td>".$row['SerialNumber']."</td>\n";
echo "<td>".$row['BatchNumber']."</td>\n";
echo "<td><a href='?id=$id'>Правка</a> </td>";
echo "<td><input type='button' onclick=\"destroy('Вы уверенно хотите удалить данный результат?', 'results.php?delid=".$id."' ) \"   value='Удаление'  > </td>";

echo "<td><input type='checkbox'    > </td>";
//href='protocols.php?delid=".$id."'

echo "</tr>";
}

echo "</table>";

echo "<a href=''> Создать отчётную форму</a>  </div>";


echo makefoot();
?>
