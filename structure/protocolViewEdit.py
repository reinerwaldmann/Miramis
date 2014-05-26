__author__ = 'vasilev_is'

from classes import *
from mydbconnect import dbdesc
import pickle
from htmlgeneralfunctions import *


"""
 В этом файле описывается просмотр одногопротокола и правка протокола
 страница должна быть готова просмотреть и такой протоккол, какого нет в базе
"""



def view_protocol_by_class(protocol):
    pass

def view_protocol_by_id(id):
    """
    Просмотреть протокол по идентификатору
    :param id: в базе данных
    """
    db=dbdesc()
    cursor = db.cursor()
    sql= "Select * from protocols where id = {0} ;".format(id)
    cursor.execute (sql)  #может вытряжнуть какое-нибудь исключение

    ## Dump the results to a string
    rows = cursor.fetchall()

    if (len(rows)==0):  #если такого нет
        return "Error, no such protocol in database"
    #TODO оформить класс ошибок, которые будут появляться на экране, если что-то пошло не так

    ## Get the results
    result=rows[0]
    protocolc =pickle.loads(rows[0][3])

    return make_html_view_edit_protocol(protocolc)




def make_html_view_edit_protocol(protocol):
    """
    Отображает один протокол, предоставляет интерфейс для правки этого протокола
    :param protocol - протокол, о котором идёт речь
    """
    res = generateHTMLMetaHeader("Обзор протокола")

    res+="""
    <table border="1" style="width: 900px">
      <tbody>
        <tr>
          <th width=100px align=center  >Наименование измеряемого параметра, пункт технических требований по ТУ </br>(методов контроля)</th>
          <th width=100px align=center >Требования к режиму измерения</th>
          <th width=100px align=center >Норма по ТУ</th>
          <th width=100px align=center >Условное обозначение измеряемого параметра </th>
        </tr>
        """


    for i in (1,protocol.procedures.__len__()):
        p=protocol.procedures[i]
        res+="<tr>"+p.toHTML()
        res+="</tr>"
    res += generateHTMLFooterRep()
    return res;



#test area
def test():
    #for i, k in get_list_of_protocols().items():
    #    print (i, k)

    with open ("protocolvieweditout.html", "wb") as outhtml:
        outhtml.write (view_protocol_by_id(1).encode("utf-8"))

test()


#http://www.codeisart.ru/processing-forms-javascript/

