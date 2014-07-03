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


echo "<div align='left'> <form action='../python/FR_makereports.py' method='post'>    <table class='itemstable'>";
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
echo "<td><input type='checkbox' name='checkbox_$id' value='Yes' /> </td>";
//href='protocols.php?delid=".$id."'

echo "</tr>";
}

echo "</table>";


echo "
<script>

function cancel()
{
var divf=document.getElementById('reportformfieldsdiv');
divf.innerHTML=\"<input type='button' onclick='putDiv();'  value='Создать отчётную форму' > \";


}


function putDiv ()
{

var divf=document.getElementById('reportformfieldsdiv');

divf.innerHTML=\"<div style='border: 1px solid; width: 500px; padding: 10px;'> \
\
    <table>  \
        <tr> \
            <td> <label for='field_step'>Количество отчётов на страницу:</label> </td>   \
            <td> <input type='number' name='field_step'  value=5  min=1 max=20 >  </td>   \
        </tr>   \
        <tr> \
            <td> <label for='field_testtype'>Вид испытаний:</label> </td>   \
            <td> <input type='text' name='field_testtype' > </td>   \
        </tr>   \
        <tr>    \
            <td> <label for='field_smbsurname'>Фамилия кого-то там:</label> </td>   \
            <td> <input type='text' name='field_smbsurname' > </td> \
        </tr>   \
    </table>    \
    </br>   \
    <input type='submit' value='Создать отчёт' style='width: 200px; height: 50px; ' >  </br> \
    <input type='button' onclick='cancel();' value='Отмена' style='width: 200px;'>   \
</form> \
</div>\";



}
</script>
";


echo "<div id='reportformfieldsdiv'>  <input type='button' onclick='putDiv();'  value='Создать отчётную форму' >  </form>   </div>";
echo makefoot();
?>
