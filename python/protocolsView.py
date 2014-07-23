#!/usr/bin/python3.4
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
          <th width=100px align=center  >Номер протокола</th>
          <th width=100px align=center >Название модели</th>
          <th width=100px align=center >Название программы</th>
        </tr>
        """
    for i in listOfProtocols.keys():
        res+="<tr>  <td>{0}</td> \n   <td>{1}</td> \n   <td>{2}</td> \n    </tr> ".format(i, listOfProtocols[i].model, listOfProtocols[i].typeOfTest)
    res += generateHTMLFooterRep()
    return res







#test area
def test():
    #for i, k in get_list_of_protocols().items():
    #    print (i, k)

    with open ("htmlprotocolstest.html", "wb") as outhtml:
        outhtml.write (make_html().encode("utf-8"))


test()

