#!C:\Python33\python.exe

#-*- coding: utf-8

__author__ = 'vasilev_is'

from classes import *
import htmlgeneralfunctions as htmg
import backend_manageProtocols as bck

import cgitb, cgi, io, sys, os
cgitb.enable()

"""
Файл, предоставляющий доступ к редакции одного испытания
"""

def outGeneral(id):
    """
    Выводит то, что должно выводиться по-любому
    @id - айди протокола
    """
    out="""Content-Type: text/html;charset=utf-8\n\n
    <html lang="ru-RU">
<meta charset='UTF-8' />
<head>
    <title>Редакция испытание</title>
    <style type='text/css'>
    td#dicttable  {border:1px solid #000;}
    .c1 ,td#dicttable:first-child        {display:none;}
    </style>
<script type='text/javascript' src='../MiramisPHP/functions.js'></script>
</head>
<body>

<h2> Форма для редакции испытания </h2>

<table border='1' style='width: 100%; padding: 0px;'  >
    <tbody>
        <tr>
          <th align=center >Наименование измеряемого параметра, пункт технических требований по ТУ </br>(методов контроля)</th>
          <th align=center >Требования к режиму измерения</th>
          <th align=center >Норма по ТУ</th>
          <th align=center >Условное обозначение измеряемого параметра </th>
        </tr>

       <tr>
        <td><textarea name ='name' id='name' cols='70' rows='5'> </textarea></td>
        <td> <div id='mode_contendor'>               </div>      </td>
        <td> <div id='normal_values_contendor'>    </div>  </td>
        <td> <div id='pars_contedor'>  </div> </td>
       </tr>

      </tbody>
</table>"""

    out+="<input type='button' onclick=\"saveData('FRtestedit.py?saveid="+str(id)+"'); \"  value='Сохранить данные' >"
    out+="<input type='button' onclick='javascript:history.go(-1);'  value='Отмена' >"
    return out

def outNormalForm (id):
    """
    Выводит пустую форму.
    @id - айди протокола, в который испытание надо будет добавить
    """
    #получить протокол из базы
    #оттуда взять список каналов
    #на основе этого списка пстроить форму
    protocol = bck.getProtocolFromDatabase(id)[0];
    if protocol==None:
        return htmg.throwError("FRtestedit", "Нет такого протокола, испытание которого намереваемся править")

    listchannels = protocol.channelname
    out=" <script> \n  add_forms_to_table("+listchannels.__str__()+" ); </script>"
    return out

def outFilledForm(id, procid):
    out=outNormalForm(id)
    proc=bck.getTestFromProtocol (id, procid) # Возвращает объект испытания










    return out




def writeTestFromInputParameters(form):

    if "mode_common" in form and "mode_channel" in form and "normal_values" in form and "pars" in form and "name" in form:
        mode_common=form.getfirst("mode_common", "")
        mode_channel=form.getfirst("mode_channel", "")
        normal_values=form.getfirst("normal_values", "")
        pars=form.getfirst("pars", "")
        name=form.getfirst("name", "")

        saveid=int(form.getfirst("saveid", ""))

        prc=Procedures()

        prc.number=0
        prc.name=name
        prc.mode_common=eval(mode_common)
        prc.mode_channel=eval(mode_channel)
        prc.normal_values=eval(normal_values)
        prc.listOfPossibleResults=eval(pars)




        retval=bck.addTestToProtocol (saveid, prc, desiredid=None) #Добавить испытание в протокол
        if not retval:
            return "Испытание сохранено успешно! id="+str(saveid)
        else:
            return "Проблемы при сохранении испытания, код ошибки от addTestToProtocol: "+str(retval)



    return "Недостаточно полей для записи испытания"+form.__str__()+form.getvalue('name')




#у этой страницы могут быть три параметра - id, то есть айди протокола, есть всегда и может быть idtest - айди испытания
#ещё параметр saveid - тогда значит надо сохранить (т. е. добавить или перезаписать) введённое испытание

form = cgi.FieldStorage()

if "saveid" in form:
    htmg.out ("Content-Type: text/html;charset=utf-8\n\n")
    htmg.out(writeTestFromInputParameters(form))
    exit(0)



#вызвать сохраение данных и выйти из скрипта!

if "id" not in form:
    htmg.out(htmg.generateHTMLMetaHeader())
    htmg.out(htmg.throwError("FRtestedit.py", "Не получен ID протокола"))
    htmg.out(htmg.generateHTMLFooter())
    exit(0) #а  можно ли вообще так выходить из cgi?








id=int(form.getfirst("id", ""))

htmg.out(outGeneral(id))
htmg.out(outNormalForm (id))

htmg.out(htmg.generateHTMLFooter())








