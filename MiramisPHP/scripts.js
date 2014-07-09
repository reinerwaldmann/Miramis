function destroy(text, head)
{
if (confirm(text))
document.location.href = head;
}


function checkAll (tableid, columnn_number)
//ставит галочки во всей таблице с айди tableid. Поле с галочками должно находиться в колонке номер columnn_number
{

  var table=document.getElementById(tableid);    // Получаем указатель нужной нам таблицы




  for (var r=1; r<table.rows.length; r++) //перебор по строкам
  {
      var cls = table.rows[r].cells[columnn_number];
      var child = cls.firstElementChild;  //получили единственного потомка (галочку)

      if (table.rows[0].cells[columnn_number].firstElementChild.checked)
      child.checked = true;
      else
      child.checked = false;


  }




}