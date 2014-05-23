__author__ = 'vasilev_is'


from mydbconnect import dbdesc
import pickle
from htmlgeneralfunctions import *



def make_filters ():
    """
    Делает фильтровую строку, которая скармливается функции get_get_list_of_protocols.
    Фильтровая строка делается из праметров, введённых пользователем
    """

    pass


def get_list_of_protocols (filters=None):
    """
    возвращает список протоколов, получаемых из базы данных,
    или же словарь, где id в базе данных - объект
    filters - строка с фильтрами. Может быть None
    """
    db=dbdesc()
    cursor = db.cursor()

    if (filters==None):
        sql = "Select * from protocols;"

    else:
        sql= "Select * from protocols where {0} ;".format(filters)

    cursor.execute (sql)  #может вытряжнуть какое-нибудь исключение

    ## Dump the results to a string
    rows = cursor.fetchall()

    ## Get the results
    res=dict()
    for each in rows:
    ## The result is also in a tuple
        res[each[0]]=pickle.loads(each[3])

    return res

def make_html():
    res = generateHTMLMetaHeader("Обзор видов протоколов")

    listOfProtocols = get_list_of_protocols()  #потом  надо применить сюда фильтры, когда дело дойдёт до CGI



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
        for k in resultslist:
            res+="<td>{0}</td>".format(k.proceduresResults[p.number].toHTML())
        res+="</tr>"
        #res+= """<tr> {0} <td> </td> <td> </td> <td> </td> </tr> """.format(p.toHTML())






    res += generateHTMLFooterRep()
    return res


#test area
def test():
    #for i, k in get_list_of_protocols().items():
    #    print (i, k)


    with open ("htmlprotocolstest.html", "wb") as outhtml:
        outhtml.write (make_html().encode("utf-8"))







test()