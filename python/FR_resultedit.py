#!C:\Python33\python.exe

#-*- coding: utf-8

__author__ = 'vasilev_is'
from  classes import *
import htmlgeneralfunctions as htmg
import backend_manageProtocols as bck
import backend_manageResults as bmr
import cgitb, cgi, io, sys, os
cgitb.enable()



def outEditFormForResult(result: AResult, id):
    res=str()


    res+="<h1>Правка результата</h1>"

    #вывод справочной части
    st="<b>{0}<b>: {1}<br/>\n"

    res+=st.format("Модель", result.model)
    res+=st.format("Вид теста", result.typeOfTest)
    res+=st.format("Оператор", result.operator)
    res+=st.format("Дата и время теста", result.testDateTime)
    res+=st.format("Номер изделия", str(result.numOfProduct))
    res+=st.format("Номер партии", str(result.numOfBatch))
    res+=st.format("Прошёл ли тест", str(result.hasPassedTest))


    #вывод таблицы результатов

    res+="<br/><br/>"
    res+="<table border=1>\n"

    res+="""
    <tr>
    <th>Номер результата</th>

    <th>Пройдено ли испытание</th>

    <th>Результаты испытания</th>

    <th>Правка</th>

    <th>Удаление</th>

    </tr>"""




    for key, val in result.proceduresResults.items():
        res+="<tr>\n"

        interactive_form=val.toHTML()


        delbtn=" <input type='button' onclick=\"destroy('Вы уверенно хотите удалить данный результат?', 'FR_resultedit.py?id="+str(id)+"&delid="+str(key)+"' ) \"   value='Удаление'  >"

        res+="""<td> {0} </td> <td> {1} </td> <td> {2} </td> <td> {3} </td> <td> {4} </td>
        """.format (str(val.number)+"_"+str(key),  {True: "Пройдено", False: "Не пройдено"}[val.hasPassedProcedure], interactive_form,
                    "<a href='FR_oneresultedit.py?id="+str(id)+"&editid="+str(key)+"'>Правка</a>", delbtn)
        res+="</tr>\n"




    return res



htmg.out (htmg.generateHTMLMetaHeader("Правка результата")+"<br/><br/>" )


form = cgi.FieldStorage()
if "id" not in form:
    htmg.out (htmg.throwError("FR_resultedit.py", "Ошибка: не предоставлен id результата", errortype=None))


else:
    id=int(form.getfirst("id", ""))
    result = bmr.getResultFromDatabase(id)

    if result[0]==None:
        htmg.throwError("FR_resultedit.py", "Ошибка получения результата из БД: "+result[1], errortype=None)
    else:
        htmg.out(outEditFormForResult(result[0], id ))



htmg.out(htmg.generateHTMLFooter())
