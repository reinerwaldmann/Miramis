<?php
//session_start();
//if(session_id() != $_POST['sid']) die('Wrong Request');

$host='localhost'; // имя хоста (уточняется у провайдера)
$database='miramisdb'; // имя базы данных, которую вы должны создать
$user='root'; // заданное вами имя пользователя, либо определенное провайдером
$pswd='123'; // заданный вами пароль
 
$dbh = mysql_connect($host, $user, $pswd) or die("Не могу соединиться с MySQL.");
mysql_select_db($database) or die("Не могу подключиться к базе.");


$query = "SELECT * FROM `protocols`";
$res = mysql_query($query);


while($row = mysql_fetch_array($res))
{
echo "Номер: ".$row['ID']."<br>\n";
echo "Модель: ".$row['ProductName']."<br>\n";
echo "тест: ".$row['TestName']."<br><hr>\n";
}


?> 
  