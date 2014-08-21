/*
Этот js файл содержит функции для построения интерактивной формы на странице. Должен использоваться в комплекте с подходящим html файлом.
*/
/*
Требования к HTML:

Со стороны функции add_forms_to_table(channellist) и функций посылки данных на сервер
    addDictForm('mode_common','mode_contendor');
    addDict2DictFormChannels ('mode_channel','mode_contendor', channellist );
    addDict2DictFormChannels('normal_values','normal_values_contendor', channellist);
    addListform('pars', 'pars_contedor');
*/


////////////////////////////DICTFORM\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    function getMaxRowIdInTable(tableid)
        //получает максимальный айди из всех строк таблицы
        //tableid - айди таблицы
        //id располагается в первой колонке таблицы
    {
                var table=document.getElementById(tableid);    // Получаем указатель нужной нам таблицы
                if (table.rows.length==0) return 0;
                var maxid=0;

                for (var i=1; i<table.rows.length;i++)
                {
                var  row = table.rows[i];
                 var cell=row.cells[0];

                maxid=Math.max (maxid, parseInt(cell.innerHTML));
                }
                return maxid+1;
    }


    function rmRow(tableid, rowIndex)
    //удаляет строку из таблицы
    //tableid - айди формы
    //rowIndex - индекс строки

    {
            var table=document.getElementById(tableid);    // Получаем указатель нужной нам таблицы
            //if (table.rows.length>2)
                 table.deleteRow(rowIndex);
    }

    function insertRow(tableid, rowIndex, key="", value="")
    // Вставка новых строк в форму
    //tableid - айди формы
    //rowIndex - индекс строки
    //key - значение ключа (вторая колонка)
    //key - значение значения (третья колонка)



    {
            var table=document.getElementById(tableid);    // Получаем указатель нужной нам таблицы
            var id=getMaxRowIdInTable(tableid);
            var row = table.insertRow(table.rows.length);
            var cell0 = row.insertCell(0);
            var cell1 = row.insertCell(1);
            var cell2 = row.insertCell(2);
            var cell3 = row.insertCell(3);
            cell0.innerHTML=" "+id
            cell1.innerHTML = "<input type='text' id='"+tableid+"_key["+id+"]'  value='"+key+"'   >";
            cell2.innerHTML = "<input type='text' id='"+tableid+"_value["+id+"]' value='"+value+"' >";
            cell3.innerHTML = "<input type='button' value='[-]'  onclick=\"return rmRow('"+tableid+"',   getParent(this, 'TR').rowIndex  ) ;\"> ";


                //"<a class='controlLinkAdd' href='#'  onclick=\"return insertRow('dict1',   getParent(this, 'TR').rowIndex+1  ) ;\"   >[+&#8595 ]</a>";
                //"<a class='controlLinkAdd' href='#'  onclick=\"return insertRow('dict1',   getParent(this, 'TR').rowIndex  ) ;\"   >[+&#8593;]</a>";

    }


    function getParent(obj, parentTagName)
     //получение родителя - obj - ссылка на объект, родителя которого мы ищем parentTagName - тег родителя, которого мы ищем.  Если тега нет, вернёт null. Теги задавать в верхнем регистре!
    {
    return (obj.tagName==parentTagName)?obj:getParent(obj.parentNode, parentTagName);
    }


    function collectDataFromDictTable(dicttableId, isInD2Dform=0 )
    //функция, которая собирает все данные из таблицы и собирает их в строку Питона, отображающую словарь
    //dicttableId  айди таблицы
    {

            //в таблице 1 строка всегда по умолчанию, зачем-то
            var table=document.getElementById(dicttableId );    // Получаем указатель нужной нам таблицы
            var numrows =table.rows.length;
            var res="{";

            if (isInD2Dform==1)
             {
                if (numrows==0) return "{}";  //если нет полей, то вернуть пустую строку
             }
            else
             {
                if (numrows==0) return "{}";  //если нет полей, то вернуть пустую строку
             }



            maxid=getMaxRowIdInTable(dicttableId);
            for (var i=0; i<maxid; i++)
            {
                keyform = document.getElementById(dicttableId+"_key["+i+"]");
                valueform = document.getElementById(dicttableId+"_value["+i+"]");
                if ((keyform!=null)&&(valueform!=null ))
                {
                    keyformval=keyform.value.trim();
                    valueformval=valueform.value.trim();
                    if (keyformval&&valueformval)
                    {
                        res+="'"+keyformval+"' : '"+valueformval+"'";

                        if (i!=maxid-1)
                            { res+=" ,";}
                    }
                    else
                    {
                        if ((res[res.length-1]=="," )&& (i==maxid-1)) //если последняя запятая, и при этом вышло так, что мы на последнем элементе, тооо
                            {
                             res=res.substring(0, res.length - 2);
                            }
                    }
                }
            }

            res+="}";

            return res
    }

function addDictForm (formid, parentdivid, header='')
//добавляет форму редакции словаря
//formid - айди новой формы, то есть дива
//parentdivid - айди родительского элемента, используется обычно div, теоретически возможна работа с другими контейнерными элементами
//получается два вложенных дива - снаружи родительский, внутри див формы
{
document.getElementById(parentdivid).innerHTML=document.getElementById(parentdivid).innerHTML+addDictFormStr (formid,0,  header);
}

function addDictFormStr (formid, isInDict2Dict, header='')
//возвращает строку формы редакции словаря
//formid - айди новой формы, то есть дива
//Если параметр isInDict2Dict установлен в 1, то эта форма является частью dict2dict, и на кнопке должна быть надпись "добавить поле в категорию"
{
buttonCaption="Добавить поле";
if (isInDict2Dict==1) buttonCaption="Добавить поле в категорию";

hdr='';
if (header) hdr ='<p>'+header+'</p>';


var table = hdr+ " <table id='"+ formid +"' border='0'> "+
    "<tbody>"+
    "<col class='c1'><col span='2'>"+
    " <tr> </tr> "+
    " </tbody>"+
"</table>"+
    "<input type='button' value='"+buttonCaption+"'  onclick=\"return insertRow('"+formid +"',   1) ;\"> ";
 "<br/>";

//"<input type='button' name='submit_button' onclick=\"collectDataFromDictTable('"+formid+"')\">";
return table;
}

function fillDictForm (dict, formid)
//заполнеение формы словаря
//formid - айди формы
//dict - словарь javascript, идентичный по записи словарю Питона, которым заполняется форма. Вся предыдущая информация стирается!
{
 div = document.getElementById(formid);
 div.innerHTML="";


    for (var key in dict)
    {
         insertRow(formid, 1, key, dict[key]);

    }


}



////////////////////////////////DICT2DICTFORM\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


function addDict2DictForm (formid, parentdivid)
//добавляет форму словаря словарей
//formid - айди новой формы, то есть дива
//parentdivid - айди родительского элемента, используется обычно div, теоретически возможна работа с другими контейнерными элементами
//получается два вложенных дива - снаружи родительский, внутри див формы
{
contains="<input type='button' value='Добавить поле верхнего уровня'  onclick=\"return insertDict2DictField('"+parentdivid +"',   '') ;\"> ";
document.getElementById(parentdivid).innerHTML=document.getElementById(parentdivid).innerHTML+contains;
}


function addDict2DictFormChannels (formid, parentdivid, channellist, header='')
//добавляет форму словаря словарей, при этом создавая поля верхнего уровня с именами, взятыми из списка channellist.
//В данной версии названия каналов в этой форме не изменяются!
//formid - айди новой формы, то есть дива
//parentdivid - айди родительского элемента, используется обычно div, теоретически возможна работа с другими контейнерными элементами
//получается два вложенных дива - снаружи родительский, внутри див формы
{
    formdiv=document.createElement('div');
    formdiv.className='dict2dictformdiv';
    formdiv.id=formid;




    parentdiv=document.getElementById(parentdivid);



    if (header){

        var element = document.createElement('p');
        element.appendChild(document.createTextNode(header));
        parentdiv.appendChild (element)

    }

    parentdiv.appendChild(formdiv);


    for (var i in channellist)  //для каждого канала в списке каналов
    {
        insertDict2DictField(formid, channellist[i]);
    }
}



function insertDict2DictField (formid, fieldname="", dictfillment={})
//добавляет поле формы словаря словарей
//formid - айди формы
//fieldname - имя поля  верхнего уровня
//dictfillment - заполнение словаря нижнего уровня
{
//просто добавить к див formid инпут и применить к немму adDictForm
newfielddid=formid+"field_"+dict2dictgetnewid(formid);

input="<input type='text'  id='keygeneral"+newfielddid+"'  value='"+fieldname+"'  readonly='readonly'   >"+

// "<input type='button' value='Удалить поле верхнего уровня'  onclick=\"dict2dictRemoveField('"+ newfielddid+"' ) \"> "+
"<br/>"+addDictFormStr("table"+newfielddid, 1);
inputDiv=document.createElement('div');
inputDiv.className='dict2dictformfield';
inputDiv.id=newfielddid;
inputDiv.style="border: 1px double black; width=500px";
inputDiv.innerHTML=input;
reqdiv=document.getElementById (formid); //получаем айди формы dict2dict
reqdiv.appendChild(inputDiv);
fillDictForm (dictfillment, "table"+newfielddid);

}

function dict2dictgetnewid (formid)
//получает новый (максимальный) идентификатор для нового поля в dict2dictform
//formid - айди формы
//возвращает полученный идентификатор

{
div = document.getElementById(formid);
maxid=0;
//проехать по всем потомкам div, выдернуть номер айди, сравнить


//этот код не работает в IE до 9-й версии
var children=div.children; //все потомки div

for (var i=0; i<children.length; i++)
    {
        if (children[i].tagName=="DIV")
        {

            var splt=children[i].id.split("_");
            var idch=splt[splt.length-1];
            maxid=Math.max (maxid, parseInt(idch) )+1  ;
        }
    }
return maxid;
}


//As James said, the DOM does not support removing an object directly.
//You have to go to its parent and remove it from there.
//Javascript won't let an element commit suicide, but it does permit infanticide... (c)stackoverflow


function dict2dictRemoveField (idfield)
//удаляет поле формы dic2dict, сиречь удаляет у формы div с id=idfield
//idfield  -  айди поля формы
{
var element = document.getElementById(idfield);
element.parentNode.removeChild(element);
}


function dict2dictMakeResString(formid)
//Делает строку Питона из формы словаря словарей - предоставление словаря словарей
//formid - айди формы
//возвращает строку питона
{
    resstr="{";
    div = document.getElementById(formid);


    //этот код не работает в IE до 9-й версии
    var children=div.children; //все потомки div

    for (var i=0; i<children.length; i++)
    {
     if (children[i].tagName=="DIV")
            {

                    divstr="";
                    collecteddata="";

                    fieldchildren = children[i].children;
                    for (var j=0; j<fieldchildren.length; j++)
                        {
                            //добавляем ключ верхней категории
                            if (fieldchildren[j].id.indexOf('keygeneral')!=-1    )
                                divstr+="'"+fieldchildren[j].value+"' : ";

                        }

                    for (var j=0; j<fieldchildren.length; j++)
                        {
                            //добавляем ключ верхней категории
                            if (fieldchildren[j].id.indexOf('table')!=-1    )

                            collecteddata=collectDataFromDictTable (fieldchildren[j].id,1);

                        }

                        if (collecteddata.length>0)
                                {
                                    divstr+=collecteddata;
                                    resstr+=divstr+" , ";

                                }
            }
    }
if (resstr[resstr.length-2]=="," ) //если последняя запятая, и при этом вышло так, что мы на последнем элементе, тооо
{
    resstr=resstr.substring(0, resstr.length - 3);
}

resstr+="}";
//alert (resstr);
return resstr;
}




function fillDict2DictForm (dict2dict, formid)
//заполняет форму dict2dict form данными из словаря словарей dict2dict
//dict2dict - словарь словарей
//formid - айди формы
{
 div = document.getElementById(formid);
 div.innerHTML="";
    for (var i in dict2dict)
    {
      insertDict2DictField (formid, i, dict2dict[i]);
    }
}


////////////////////////////LISTFORM\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
//Listform  -  форма правки списка


    function insertRowListform(tableid, rowIndex=1, value="")
    // Вставка новых строк в форму
    //tableid - айди формы
    //rowIndex - индекс, который вставлять - данный параметр не используется!
    //value="" - значение поля
    {
            var table=document.getElementById(tableid);    // Получаем указатель нужной нам таблицы
            var id=getMaxRowIdInTable(tableid);
            var row = table.insertRow(table.rows.length);
            var cell0 = row.insertCell(0);
            var cell1 = row.insertCell(1);
            var cell2 = row.insertCell(2);
            cell0.innerHTML=" "+id
            cell1.innerHTML = "<input type='text' id='"+tableid+"_item["+id+"]' value='"+value+"'  >";
            cell2.innerHTML = "<input type='button' value='[-]'  onclick=\"return rmRow('"+tableid+"',   getParent(this, 'TR').rowIndex  ) ;\"> ";
    }


function addListformStr (formid)
//возвращает строку формы редакции списка
//formid - айди формы

{
buttonCaption="Добавить пункт списка";
var table = " <table id='"+ formid +"' border='0'> "+
    "<tbody>"+
    "<col class='c1'><col span='2'>"+
    " <tr> </tr> "+
    " </tbody>"+
"</table>"+
    "<input type='button' value='"+buttonCaption+"'  onclick=\"return insertRowListform('"+formid +"',   1) ;\"> ";
 "<br/>";

//"<input type='button' name='submit_button' onclick=\"collectDataFromDictTable('"+formid+"')\">";

return table;
}

function addListform (formid, parentdivid)
//добавляет форму словаря словарей
//formid  -  айди формы (будет div внутри div-а)
//parentdivid - айди родительского контейнера
{
document.getElementById(parentdivid).innerHTML=document.getElementById(parentdivid).innerHTML+addListformStr(formid);
}

function ListformMakeResString(dicttableId )  //в таблице 1 строка всегда по умолчанию, зачем-то
//получает строку результата - строковое представление списка, актуально в Питоне и в JavaScript
//dicttableId - айди формы
//возвращает строку результата
    {


            var table=document.getElementById(dicttableId );    // Получаем указатель нужной нам таблицы
            var numrows =table.rows.length;
            var res="[";
            if (numrows==0) return "[]";  //если нет полей, то вернуть пустую строку

            maxid=getMaxRowIdInTable(dicttableId);
            for (var i=0; i<maxid; i++)
            {
                item = document.getElementById(dicttableId+"_item["+i+"]");

                if (item!=null)
                {

                    itemval=item.value.trim();

                    if (itemval)
                    {

                        res+="'"+itemval+"'";



                        if (i!=maxid-1)
                            { res+=" ,";}
                    }
                    else
                    {
                        if ((res[res.length-1]=="," )&& (i==maxid-1)) //если последняя запятая, и при этом вышло так, что мы на последнем элементе, тооо
                            {
                             res=res.substring(0, res.length - 2);
                            }
                    }
                }
            }

            res+="]";



            return res
    }


function fillListform(fillinglist, formid)
//заполняет форму списка  данными из списка собственно
//fillinglist - список, которым заполнять
//formid - айди формы, которую заполнять
{
 div = document.getElementById(formid);
 div.innerHTML="";

    for (var i in fillinglist)
    {
        insertRowListform(formid, 1, fillinglist[i]);
    }
}


///////////////////FILLING NAME FIELD\\\\\\\\\\\\\\\\\\\\\\\\\\\\

function setname(newname, nameid)
//заполняет поле имени испытания
{
name=document.getElementById(nameid);
name.innerHTML=newname;
}


///////////////////ADDING FUNCS TO THE FORM\\\\\\\\\\\\\\\\\\\\\\\\

function add_forms_to_table(channellist)
//добавление форм в таблицу
//channellist - список каналов, на основе которых формируются формы
{
    addDictForm('mode_common','mode_contendor', 'Общие режимы');
    addDict2DictFormChannels ('mode_channel','mode_contendor', channellist, 'Поканальные режимы' );

    addDict2DictFormChannels('normal_values','normal_values_contendor', channellist, 'Поканальные нормы:');
    addDictForm('normal_values_common','normal_values_contendor', 'Общие нормы:');





    div = document.getElementById('pars_contedor');
    div.innerHTML=div.innerHTML+"Общие измерения:<br/>";

    addListform('listOfPossibleResultsCommon', 'pars_contedor');

    div.innerHTML=div.innerHTML+"<br/>Поканальные измерения:<br/>";

    addListform('pars', 'pars_contedor');
}

///////////////////SENDING DATA TO SERVER\\\\\\\\\\\\\\\\\\\\\\\\

var request;
   function getAjaxInfo(actionserver)
   //посылает данные из форм на сервер. Данные пересылаются методом POST
   //actionserver - URL куда посылать

   //так как пересылка идёт AJAX-ом, то URL должен быть в том же домене, что и страница, вызвавшая данную функцию
   //Данные - что посылать описываются в данной функции

	{

    var method="POST";
    var name=document.getElementById("name").value;
    var mode_common=collectDataFromDictTable ('mode_common');
    var mode_channel=dict2dictMakeResString ('mode_channel');

    var normal_values=dict2dictMakeResString ('normal_values');
    var normal_values_common=collectDataFromDictTable ('normal_values_common');


    var pars=ListformMakeResString ('pars');
    var listOfPossibleResultsCommon=ListformMakeResString ('listOfPossibleResultsCommon');


     var params = 'name=' + encodeURIComponent(name) +
                '&mode_common=' + encodeURIComponent(mode_common)+
                '&mode_channel=' + encodeURIComponent(mode_channel)+
                '&normal_values=' + encodeURIComponent(normal_values)+
                '&normal_values_common=' + encodeURIComponent(normal_values_common)+
                '&pars=' + encodeURIComponent(pars)+
                '&listOfPossibleResultsCommon=' + encodeURIComponent(listOfPossibleResultsCommon)
                ;





    /*collectedDataString="'mode_common'='"+mode_common+"'";
    collectedDataString+="&";


    collectedDataString+="'name'='"+name.innerText+"'";

    collectedDataString+="&";
*/
/*
    collectedDataString+="mode_channel="+mode_channel;
    collectedDataString+="&";
    collectedDataString+="&";
    collectedDataString+="normal_values="+normal_values;
    collectedDataString+="&";
    collectedDataString+="pars="+pars;
*/
    //alert (params);

    //collectedDataString=escape(collectedDataString);

    request.open(method, actionserver, true);
    request.onreadystatechange = updatePage;
    request.setRequestHeader("Content-type","application/x-www-form-urlencoded"); //не уверен, что правильно
    request.send(params);
   }

function updatePage()
//Функция, запускаемая при ответе сервера на запрос. Должна, вообще говоря, вести на страницу с протоколом
{
      if (request.readyState == 4) {
	if (request.status == 200) {
        //alert (request.responseText);
        //alert ("Данные сохранены успешно")
        var gotValue = request.responseText;
        alert(gotValue);


        var spllist, id
        if (gotValue.indexOf("Испытание сохранено успешно") > -1)
        {
            spllist=gotValue.split("=");
            id=parseInt(spllist[spllist.length-1]);
        }

        document.location.replace("FRprotocolViewEdit.py?id="+id);


        //document.getElementById("gotvalues").value = gotValue;
        //здесь надо перейти  на страницу с протоколом обратно
     }

	else alert ("server unreachable"+request.status)
	}
   }




function saveData(actionserver)
//сохраняет данные на сервер. ЭТА ФУНКЦИЯ И ДОЛЖНА ВЫЗЫВАТЬСЯ ПО КНОПКЕ!
//actionserver - имя сервера

{
    request = null;
   try {
     request = new XMLHttpRequest();
   } catch (trymicrosoft) {
     try {
       request = new ActiveXObject("Msxml2.XMLHTTP");
     } catch (othermicrosoft) {
       try {
         request = new ActiveXObject("Microsoft.XMLHTTP");
       } catch (failed) {
         request = null;
       }
     }
   }


   if (request == null)
     alert("Error creating request object!");


    getAjaxInfo(actionserver, request);

}

