#!/usr/bin/python3.4
#-*- coding: utf-8

__author__ = 'vasilev_is'
from  classes import *
import htmlgeneralfunctions as htmg
import backend_manageProtocols as bck
import backend_manageResults as bmr
import cgitb, cgi, io, sys, os
cgitb.enable()

#mätrapporter ledningssystem   - på svenska

def insertTestsAccToProtocol(idres):
    """
    Вставляет в результат пустые результаты испытаний, согласно протоколу
    @idres - айди результата
    """
    resultt = bmr.getResultFromDatabase(idres)
    if resultt[0]==None:
        return 1, "Ошибка получения результата из БД idres="+str(idres)

    result = resultt[0]
    protocolt = bck.getProtocolFromDatabaseParams (result.model, result.typeOfTest)

    if protocolt[0]==None:
        return 2, "Ошибка получения протокола из БД idres="+protocolt[1]

    protocol = protocolt[0]

    for procedurekey in protocol.procedures: #для каждой процедуры из списка оных в протоколе
        if not procedurekey in result.proceduresResults.keys(): #если процедура прописана в протоколе, но не имеется  в результате
            protocolitem = protocol.procedures[procedurekey] #получаем описание процедуры в протоколе
            newrp = resultsOfProcedure() #создаём объект результата процедуры
            newrp.number=procedurekey #копируем номер
            newrp.hasPassedProcedure=False #устанавливаем флаг, успешна ли процедура
            newrp.values1=dict() #объявляем значения словарём

            newrp.values_common=dict()  #словарь название параметра-значение для общих величин

            #заполнение значений у общих величин
            for possibleres in protocolitem.listOfPossibleResultsCommon:
                newrp.values_common[possibleres]=0



            #заполнение значений у поканальных величин
            for channel in protocolitem.normal_values: #для каждого канала
                newrp.values1[channel]=dict() #объявляем  словарём
                for possibleres in protocolitem.listOfPossibleResults: #и для каждого возможного  результата
                    newrp.values1[channel][possibleres]=0 #впихиваем нулевое значение

            result.proceduresResults[procedurekey]=newrp #теперь вгоняем новый результат в процидурку
    return bmr.writeResultToDatabase(result, idres) # и пишем в базу!


def outResultsOfProcedureForm (rop: resultsOfProcedure, prefix: str):
    """
    Выводит форму редакции одного результата как часть формы
    """
    outstr=""

    chlist = list(rop.values1.keys())
    chlist.sort()


    #for channel in rop.values1:
    for channel in chlist:
        outstr+="<b>{0}</b><br/>\n".format(channel)
        outstr+="<table>\n"

        parlist = list(rop.values1[channel].keys())

        parlist.sort()
        for parameter in parlist:

        #for parameter in rop.values1[channel]:

            inpstr="<input type='text' name='{0}' value='{1}' >".format(str(prefix)+"_"+channel+"_"+parameter, str(rop.values1[channel][parameter]))
            outstr+="<tr> <td> {0} </td> <td> {1} </td> </tr> \n".format(parameter, inpstr)

        outstr+="</table>\n"

    outstr+="<table>\n"


    if rop.values_common:
        outstr+="<b>{0}</b><br/>\n".format("Общие:")

    parlist = list(rop.values_common.keys())
    parlist.sort()

    #for parameter in rop.values_common:
    for parameter in parlist:

        inpstr="<input type='text' name='{0}' value='{1}' >".format(str(prefix)+"_"+"common&&&"+"_"+parameter, str(rop.values_common[parameter]))
        outstr+="<tr> <td> {0} </td> <td> {1} </td> </tr> \n".format(parameter, inpstr)

    outstr+="</table>\n"



    return outstr



# <input type="radio" name="browser" value="ie"> Internet Explorer<Br>
#    <input type="radio" name="browser" value="opera"> Opera<Br>
# format(str(prefix)+"_"+channel+"_"+parameter, str(rop.values1[channel][parameter]))



def outfilledformforpassed(keyOfProcedure, hasPassedProcedure):
    """
    Вывести форму для редакции "Пройдено - не пройдено"
    """
    name=str(keyOfProcedure)+"_"+"hasPassedProcedure"
    if hasPassedProcedure:
        return """
         <input type='radio' name='{0}' value='1' checked='checked'> Прошёл <Br>
         <input type='radio' name='{0}' value='0'> Не прошёл <Br>
        """.format(name)
    else:
        return """
         <input type='radio' name='{0}' value='1'> Прошёл <Br>
         <input type='radio' name='{0}' value='0' checked='checked'> Не прошёл <Br>
        """.format(name)



def outEditFormForResultOld(result: AResult, id):


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
    res+="<form action='FR_resultedit.py?id={0}&saveid={1}' method='post'> <table border=1>\n".format(str(id), str(id))
    res+="""
    <tr>
    <th>Номер результата</th>
    <th>Пройдено ли испытание</th>
    <th>Результаты испытания</th>

    <th>Удаление</th>
    </tr>"""
    for key, val in result.proceduresResults.items():
        res+="<tr>\n"
        interactive_form=outResultsOfProcedureForm (val, key)
        delbtn=" <input type='button' onclick=\"destroy('Вы уверенно хотите удалить данный результат?', 'FR_resultedit.py?id="+str(id)+"&delid="+str(key)+"' ) \"   value='Удаление'  >"
        res+="""<td> {0} </td> <td> {1} </td> <td> {2} </td> <td> {3} </td>
        """.format (str(key),  {True: "Пройдено", False: "Не пройдено"}[val.hasPassedProcedure], interactive_form,
                     delbtn)
        res+="</tr>\n"
    res+="</table> <br/> <input type='submit' value='Сохранить'>    </form>"
    res+="<a href='FR_resultedit.py?id={0}&magic={1}'> Добавить надостающие испытания в результат из протокола </a>".format(id, id)
    return res


def outEditFormForResult(result: AResult, id):

    """
    Выводит форму отображения и редакции результата.
    в этой версии выводит вместе с данными из протокола,  такими, как название и такое прочее
    """

    protocolt = bck.getProtocolFromDatabaseParams (result.model, result.typeOfTest)

    if protocolt[0]==None:
        htmg.out (htmg.throwError("FR_resultedit.py", "Ошибка при поиске протокола, соответствующего данному результату "+protocolt[1]))
        return outEditFormForResultOld(result, id)


    protocol = protocolt[0]

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
    res+="<form action='FR_resultedit.py?id={0}&saveid={1}' method='post'> <table border=1>\n".format(str(id), str(id))
    res+="""
    <tr>
    <th>Название испытания</th>
    <th>Режим испытания</th>
    <th>Нормы на испытание</th>
    <th>Пройдено ли испытание</th>
    <th>Результаты испытания</th>

    <th>Удаление</th>
    </tr>"""

    klist = list(result.proceduresResults.keys())
    klist.sort()

    for key in klist:

    #for key, val in result.proceduresResults.items():
        val = result.proceduresResults[key]
        res+="<tr>\n"
        interactive_form=outResultsOfProcedureForm (val, key)
        delbtn=" <input type='button' onclick=\"destroy('Вы уверенно хотите удалить данный результат?', 'FR_resultedit.py?id="+str(id)+"&delid="+str(key)+"' ) \"   value='Удаление'  >"
        res+="""{0} <td> {1} </td> <td> {2} </td> <td> {3} </td>
        """.format (protocol.procedures[key].toHTML(0), outfilledformforpassed(key, val.hasPassedProcedure), interactive_form,
                     delbtn)

        #{True: "Пройдено", False: "Не пройдено"}[val.hasPassedProcedure]

        res+="</tr>\n"
    res+="</table> <br/> <input type='submit' value='Сохранить'>    </form>"
    res+="<a href='FR_resultedit.py?id={0}&magic={1}'> Добавить надостающие испытания в результат из протокола </a>".format(id, id)
    return res


def savedata (saveid, form):
    resultt = bmr.getResultFromDatabase(saveid)
    if resultt[0]==None:
        return 1, "Ошибка получения результата из БД saveid="+str(saveid)
    import copy
    result=copy.deepcopy(resultt[0])


    for key in result.proceduresResults:


        ifpassedstr = str(key)+"_hasPassedProcedure"
        if ifpassedstr in form:

            try:
                result.proceduresResults[key].hasPassedProcedure=int(form.getfirst(ifpassedstr, ""))==1



                # if int(form.getfirst(ifpassedstr, ""))==1:
                #     result.proceduresResults[key].hasPassedProcedure=True
                # else:
                #     result.proceduresResults[key].hasPassedProcedure=False
                #


            except BaseException:
                return 2, "ошибка при записи значения"
        else:
            return 3, "ошибка при записи значения, возможно значение не задано"


        for channel in result.proceduresResults[key].values1:
            for parameter in result.proceduresResults[key].values1[channel]:

                inpstr=str(key)+"_"+channel+"_"+parameter

                if inpstr in form:
                    try:
                        result.proceduresResults[key].values1[channel][parameter]=float(form.getfirst(inpstr, ""))

                    except BaseException:
                        return 2, "ошибка при записи значения"
                else:
                    return 3, "ошибка при записи значения, возможно значение не задано"


        for parameter in result.proceduresResults[key].values_common:
            inpstr=str(key)+"_"+"common&&&"+"_"+parameter
            if inpstr in form:
                    try:
                        result.proceduresResults[key].values_common[parameter]=float(form.getfirst(inpstr, ""))

                    except BaseException:
                        return 4, "ошибка при записи значения (общего)"
            else:
                return 5, "ошибка при записи значения (общего), возможно значение не задано"


    wrtdb=bmr.writeResultToDatabase(result, idresult=saveid)
    if wrtdb:
        return 4, "Ошибка записи р. в БД "+str(wrtdb)



#    inpstr="<input type='text' name='{0}' value='{1}' >".format(str(prefix)+"_"+channel+"_"+parameter, str(rop.values1[channel][parameter]))


    return 0, "" #признак успешности операции




htmg.out (htmg.generateHTMLMetaHeader("Правка результата")+"<br/><br/>" )
form = cgi.FieldStorage()
if "id" not in form:
    htmg.out (htmg.throwError("FR_resultedit.py", "Ошибка: не предоставлен id результата", errortype=None))

else:
    id=int(form.getfirst("id", ""))


    if "magic" in form:
        magicres = insertTestsAccToProtocol(id)
        if magicres:
            htmg.out (htmg.throwError("FR_resultedit.py", "Ошибка при добавлении недостающих испытаний "+magicres, errortype=None))



    if "delid" in form:  #запустить сохранение
        delid=int(form.getfirst("delid", ""))

        dlitem=bmr.delItemFromResult(id, delid)
        if dlitem:
            htmg.out (htmg.throwError("FR_resultedit.py", "Ошибка при удалении результата испытания: "+dlitem, errortype=None))




    if "saveid" in form:  #запустить сохранение
        saveid=int(form.getfirst("saveid", ""))

        svd=savedata (saveid, form)
        if svd[0]:
            htmg.out (htmg.throwError("FR_resultedit.py", "Ошибка при сохранении данных: "+svd[1], errortype=None))
        #else:
        #    htmg.out (htmg.throwError("FR_resultedit.py", "Данные сохранены успешно!"+svd[1], errortype=None))


    result = bmr.getResultFromDatabase(id)

    if result[0]==None:
        htmg.throwError("FR_resultedit.py", "Ошибка получения результата из БД: "+result[1], errortype=None)
    else:
        htmg.out(outEditFormForResult(result[0], id ))



htmg.out(htmg.generateHTMLFooter())
