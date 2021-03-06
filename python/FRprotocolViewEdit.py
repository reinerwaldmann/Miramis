#!/usr/bin/python3.4
#!/usr/bin/python3.4

#-*- coding: utf-8

__author__ = 'vasilev_is'

from classes import *
import htmlgeneralfunctions as htmg
import backend_manageProtocols as bck

import cgitb, cgi, io, sys, os
cgitb.enable()





"""
Файл, предоставляющий доступ к просмотру и редакции одного протокола.
"""
#[FRONTEND DIRECT]



def outReportsParametersCombo (protocol: AProtocol, id):
    res=str()
    res+="<h3>Параметры выходных отчётов </h3>"
    res+="""\n\n<form action = 'FR_ReportParametersEdit.py?id={0}'  method='GET' > \n <select name='name'>"""



    for key in protocol.dictOfReportFormParameters.keys():
        res+="<option value = '{0}'> {0} </option> \n".format(key)

    #res+="<option value = {0} > {1} </option> \n".format("", "Создать параметры")

    res+= "</select> <br/> <input type='submit' value='Редактировать' > <input type='hidden' name='id' value='{0}'>  </form>".format(id)

    res+= "<br/> <input type='button' value='Создать' onclick=\"location.href = 'FR_ReportParametersEdit.py?id={0}'       \"> ".format(id)


    return res



def view_protocol_by_id(id):
    gotval = bck.getProtocolFromDatabase (id)
    if gotval[0]==None:
        return htmg.throwError("FRProtocolViewEdit", "В базе данных нет такого протокола id="+str(id))
    return make_html_view_edit_protocol(id, gotval[0], gotval[1], gotval[2]) + outReportsParametersCombo (gotval[0], id)


def make_html_view_edit_protocol(id, protocol, productname="", testname=""):
    """
    Отображает один протокол, предоставляет интерфейс для правки этого протокола
    :param protocol - протокол, о котором идёт речь
    """
    res =""


    res+="""<h1> Правка протокола </h1>
    """
    res+="<b> Справочная часть</b></br>"
    res+="<b>Название изделия: "+productname+"</br>"
    res+="<b>Название теста: "+testname+"</br></br></br>"
    res+="""
    <table border="1" style="width: 900px">
      <tbody>
        <tr>
          <th width=100px align=center  >Наименование измеряемого параметра, пункт технических требований по ТУ </br>(методов контроля)</th>
          <th width=100px align=center >Требования к режиму измерения</th>
          <th width=100px align=center >Норма по ТУ</th>
          <th width=100px align=center >Условное обозначение измеряемого параметра </th>
          <th width=100px> </th>
          <th width=100px> </th>
        </tr>
        """
#protocol.procedures - это словарь. Посему делать надлежит далеко не так
    #for i in (1,protocol.procedures.__len__()):
    keys=protocol.procedures.keys()
    for i in keys:
        p=protocol.procedures[i]
        res+="<tr>"+p.toHTML()
        res+="<td> <input type='button' onclick=\"destroy('Вы уверенно хотите удалить данное испытание?', 'FRprotocolViewEdit.py?id="+str(id)+"&delid="+str(i)+"' ) \"   value='Удаление'  > </td>  "
        res+="<td> <a href='FRtestedit.py?id="+str(id)+"&testedit="+str(i)+"'>Правка</a></td>"
        res+="</tr>"

    res+="</tbody>    </table>"
    res+="<a href='FRtestedit.py?id="+str(id)+"'>Создать испытание</a>"

#    res += htmg.generateHTMLFooterRep()
    return res;



#test area
def test():
   # with open ("../html/protocolvieweditout.html", "wb") as outhtml:
    #    outhtml.write (view_protocol_by_id(1).encode("utf-8"))
    print (view_protocol_by_id(1).encode("utf-8"))
 #   with open ("protocolvieweditout1.html", "wb") as outhtml:
  #      outhtml.write (view_protocol_by_id(1).encode("utf-8"))



#out("Content-Type: text/html;charset=utf-8\n\n")
#out("<html><head>\n\n")
#out("</head><body>\n\n")

#узнаём, есть ли айди в параметрах

form = cgi.FieldStorage()


#TODO: вызов добавления результата по протоколу



htmg.out (htmg.generateHTMLMetaHeader("Обзор протокола"))
if "id" not in form:
    htmg.out (htmg.throwError("FRprotocolViewEdit.py", "Ошибка: не предоставлен id протокола", errortype=None))
else:
    id=int(form.getfirst("id", ""))

    if ("delid") in form:
        delid=int(form.getfirst("delid", ""))
        bck.delTestFromProtocol(id, delid)
        htmg.out("Испытание удалено успешно!"+str(id)+"  "+str(delid))
        htmg.out("<script> document.location.replace('FRprotocolViewEdit.py?id="+str(id)+"');</script>")
    htmg.out (view_protocol_by_id(id))


htmg.out(htmg.generateHTMLFooter())


htmg.out(htmg.generateHTMLFooter())



#http://www.codeisart.ru/processing-forms-javascript/


