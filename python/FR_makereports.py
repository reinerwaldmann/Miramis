#!/usr/bin/python3.4
#-*- coding: utf-8

__author__ = 'vasilev_is'
from  classes import *
import htmlgeneralfunctions as htmg
import backend_manageProtocols as bck
import backend_manageResults as bmr
import parsers as prs
import cgitb, cgi, io, sys, os
cgitb.enable()

"""
Данный скрипт делает групповые отчёты и выводит их в html формате
(пока так, потом, возможно, в зависимости от настроек, и в pdf)

"""


#начинаем создавать хытымыль-страницу
#хытымыль страница состоит из шапки и главной части по одной классификации
#и из программы испытаний и протокола испытаний по другой классификации
#главная часть состоит из процедур, каждая из которых генерируется отдельно
#каждая процедура состоит из левой и правой части. Левая часть заполняется из программы испытаний, правая часть заполняется из протокола испытаний


def generateHTMLOLD (resultslist:list, protocol:AProtocol, form):
    """
    @resultslist список результатов
    @protocol протокол

    Генерирует тело таблицы
    """
    if (resultslist == None):
        htmg.throwError("makereports", "Ошибка, None как список резльутатов")
        return ""

    if (protocol == None):
        htmg.throwError("makereports", "Ошибка, None как протокол")
        return ""

    if (resultslist.__len__==0):
        htmg.throwError("makereports", "Нет результатов в списке!")
        return ""


    res=generageHTMLProtocolHeader(resultslist.__len__(), resultslist[0], form)
    #res+=generageHTMLProtocolHeader(resultslist[0])  #resultslist - это список результатов. Результатов всегда список, тогда как протокол - один
    #таблица пошла

    #Здесь можно напистаьпроверку на соответствие результатов протоколу

    for i in protocol.procedures.keys():
        p=protocol.procedures[i]
        res+="<tr>"+p.toHTML()
        for k in resultslist:
            if i in k.proceduresResults.keys():
                res+="<td>{0}</td>".format(k.proceduresResults[i].toHTML())
            else:
                res+="<td> </td>"
        res+="</tr>"
        #res+= """<tr> {0} <td> </td> <td> </td> <td> </td> </tr> """.format(p.toHTML())


    res += htmg.generateHTMLFooterRep()
    return res


def generateHTML (resultslist:list, protocol:AProtocol, form):
    """
    @resultslist список результатов
    @protocol протокол

    Генерирует тело таблицы
    """
    if (resultslist == None):
        htmg.throwError("makereports", "Ошибка, None как список резльутатов")
        return ""

    if (protocol == None):
        htmg.throwError("makereports", "Ошибка, None как протокол")
        return ""

    if (resultslist.__len__==0):
        htmg.throwError("makereports", "Нет результатов в списке!")
        return ""


    res=generageHTMLProtocolHeader(resultslist.__len__(), resultslist[0], form)
    #res+=generageHTMLProtocolHeader(resultslist[0])  #resultslist - это список результатов. Результатов всегда список, тогда как протокол - один
    #таблица пошла

    #Здесь можно напистаьпроверку на соответствие результатов протоколу

    for i in protocol.procedures.keys():
        p=protocol.procedures[i]
        res+="<tr>"+p.toHTML()
        for k in resultslist:
            if i in k.proceduresResults.keys():
                res+="<td>{0}</td>".format(k.proceduresResults[i].toHTML())
            else:
                res+="<td> </td>"
        res+="</tr>"
        #res+= """<tr> {0} <td> </td> <td> </td> <td> </td> </tr> """.format(p.toHTML())


    res += htmg.generateHTMLFooterRep()
    return res



def generageHTMLProtocolHeader(numOfProducts, result, form):
    """
    @numOfProducts число изделий
    @result один из результатов (оттуда списывается модель и дата теста)
    Создаёт голову таблицы
    """

    typeofthetest=form.getfirst("field_testtype", "")

    res="<div align='center'> <p>ПРОТОКОЛ №  от "+result.testDateTime+"</p>  "
    res+="<p>"+typeofthetest+"</p>"
    res+="<p>"+result.model+"</p>"

    strnumprs=""
    for x in range (1, numOfProducts+1):
        strnumprs+="<td align=center >{0}</td>\n".format(x)

    res+= """

    <table border="1" style="width: 900px">
      <tbody>
        <tr>
          <th width=100px align=center  rowspan=3>Наименование измеряемого параметра, пункт технических требований по ТУ </br>(методов контроля)</th>
          <th width=100px align=center rowspan=3>Требования к режиму измерения</th>
          <th width=100px align=center rowspan=3>Норма по ТУ</th>
          <th width=100px align=center rowspan=3>Условное обозначение измеряемого параметра </th>
          <th align=center colspan={0}>Результаты измерений</th>
        </tr>
        <tr>
          <td align=center  colspan={0}>Номер ИВЭП</td>
        </tr>
        <tr>
          {1}
        </tr>

    """.format(numOfProducts, strnumprs)
    return res





def outreport (residlist, form):
    errlog=str()

    reslist=list()
    for resid in residlist:
        res = bmr.getResultFromDatabase(resid)  # Получить результат из базы данных
        if res[0]==None:
            errlog+="Ошибка: такого результата нет в базе данных"
        else:
            reslist.append(res[0])

    if len(reslist)==0: #если список результатов пуст, это из-за всяких ошибок может быть
        return "", errlog



    for result in reslist: #проверяем список результатов на однородность, то есть все результаты должны быть от одного протокола
        if not result.model==reslist[0].model or not result.typeOfTest==reslist[0].typeOfTest:
            errlog+="Ошибка: в выборке присутствуют результаты от разных протоколов"
            return "", errlog


    prot = bck.getProtocolFromDatabaseParams (reslist[0].model, reslist[0].typeOfTest)
    if prot[0]==None:
         errlog+="Ошибка: в базе данных нет протокола под такой результат"
         return "", errlog

    protocol=prot[0]


    return generateHTML (reslist, protocol, form), errlog



    #bck.getProtocolFromDatabaseParams (ProductName, TestName)





def outreportsgroup (residlist, form):

    step=int(form.getfirst("field_step", ""))


    res=str()
    err=str()

    for i in range (0, len(residlist), step):
        outr=outreport(residlist[i:i+step], form)
        res+=outr[0]+"<br style='page-break-after: always'> "
        err+=outr[1]


    return res + err




htmg.out (htmg.generateHTMLMetaHeader("Вывод отчётной формы", 0))

#получение списка результатов для построения отчётов
form = cgi.FieldStorage()
residlist=list()
#making results list:
for key in form:
    #htmg.out(key+"  "+ form.getfirst(key, "")   +"</br>")
    if "checkbox" in key:
        residlist.append(int(key.split("_")[1]))

if len(residlist)>0:
    htmg.out(outreportsgroup(residlist, form))  #если список не пуст, вывести группу отчётов




htmg.out(htmg.generateHTMLFooter())


#Как ставить номер протокола? Добавить поля вид протокола (ОТК), вид испытаний (Предъявительские)
#Дату надо парсить в нормальный формат
#http://dik123.blogspot.ru/2009/02/html-pdf.html
#На этой странице написано, как переводить html-документы в pdf
