__author__ = 'vasilev_is'

from classes import *
import htmlgeneralfunctions as htmg
import backend_manageProtocols as bck


"""
Файл, предоставляющий доступ к просмотру и редакции одного протокола.
"""
#[FRONTEND DIRECT]


#TODO: Сделать функцию, отображающую один протокол (справочную часть и испытания)
#TODO: вызов правки испытания
#TODO: вызов удаления испытания
#TODO: вызов добавления испытания
#TODO: вызов добавления результата по протоколу

def view_protocol_by_id(id):
    gotval = bck.getProtocolFromDatabase (id)
    if gotval[0]==None:
        return htmg.throwError("FRProtocolViewEdit", "В базе данных нет такого протокола id="+str(id))
    return make_html_view_edit_protocol(gotval[0], gotval[1], gotval[2])


def make_html_view_edit_protocol(protocol, productname="", testname=""):
    """
    Отображает один протокол, предоставляет интерфейс для правки этого протокола
    :param protocol - протокол, о котором идёт речь
    """
    res = htmg.generateHTMLMetaHeader("Обзор протокола")


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
        res+="<td> <input type='button' onclick=\"destroy('Вы уверенно хотите удалить данное испытание?', 'protocols.php?delid="+str(i)+"' ) \"   value='Удаление'  > </td>  "
        res+="<td> <a href=''>Правка</a></td>"
        res+="</tr>"
    res += htmg.generateHTMLFooterRep()
    return res;



#test area
def test():


    with open ("../html/protocolvieweditout.html", "wb") as outhtml:
        outhtml.write (view_protocol_by_id(1).encode("utf-8"))



 #   with open ("protocolvieweditout1.html", "wb") as outhtml:
  #      outhtml.write (view_protocol_by_id(1).encode("utf-8"))




test()


#http://www.codeisart.ru/processing-forms-javascript/

