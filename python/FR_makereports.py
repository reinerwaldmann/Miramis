#!/usr/bin/python3.4
#!/usr/bin/python3.4
#!/usr/bin/python3.4
#!/usr/bin/python3.4
#!/usr/bin/python3.4
#-*- coding: utf-8

__author__ = 'vasilev_is'
from  classes import *
import htmlgeneralfunctions as htmg
import backend_manageProtocols as bck
import backend_manageResults as bmr
import parsers as prs
import datetime
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

def sortResultsBySerial(input):
    return input.numOfProduct


def generateOneReportFooter (form, resultslist:list):
    """
    :param form: форма post, пришедшая от пользователя
    :param resultslist: список результатов
    :return: строку футера одного отчёта
    """
    res=""

    numOfPrInGroup = len(resultslist)

    numOfPassed=len(list( filter(lambda x: x.hasPassedTest, resultslist)))

    numOfFailed = numOfPrInGroup-numOfPassed

    spdict= {"RK":"ОТК", "OTK": "ВП", "VP": "____"}

    # Делаем вот такой словарь. Затем ищем то, что в типе теста после _, и это то пытаемся применить как ключ.
    #


    try:
        out = spdict[resultslist[0].typeOfTest[resultslist[0].typeOfTest.rfind("-")+1::].strip()]
    except BaseException:
        out="____"


    return """Из партии {0} шт. проверено {1} шт. из которых: \n  <br/>
    {2} шт. соотвутствуют НТД и подлежат предъявлению в {3}, {4} шт. отошли при испытаниях. \n <br/>
    Испытания проводил _______________________________. Начато ______________________. Окончено ______________________.
     """.format ("______", numOfPrInGroup, numOfPassed, out,  numOfPassed, numOfFailed)


def generateHTML (resultslist:list, protocol:AProtocol, form, name=None):
    """
    @resultslist список результатов
    @protocol протокол

    @name - имя набора параметров отчёта

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

#отсортируем выводимые по серийничку
    resultslist.sort(key=sortResultsBySerial)

    res=generageHTMLProtocolHeader(resultslist.__len__(), resultslist[0], form, resultslist)
    #res+=generageHTMLProtocolHeader(resultslist[0])  #resultslist - это список результатов. Результатов всегда список, тогда как протокол - один
    #таблица пошла

    #Здесь можно напистаьпроверку на соответствие результатов протоколу

    #ReportFormParameters



    # try:
    #     rfp=protocol.dictOfReportFormParameters[name]
    # except BaseException:
    #     rfp=None

    #rfp - ReportFormParameters




    for i in protocol.procedures.keys():
        p=protocol.procedures[i]

        prfp=None
        try:
            prfp=protocol.dictOfReportFormParameters[name].dictOfProceduresParameters[i]
        except BaseException:
            prfp=None

        #получили ProcedureReportFormParameters, если он есть



        res+="<tr>"+p.toHTML(prfp=prfp)

        for k in resultslist:
            if i in k.proceduresResults.keys():
                res+="<td>{0}</td>".format(k.proceduresResults[i].toHTML(prfp))
            else:
                res+="<td> </td>"
        res+="</tr>"
        #res+= """<tr> {0} <td> </td> <td> </td> <td> </td> </tr> """.format(p.toHTML())


    res += htmg.generateHTMLFooterRep()
    return res



def generageHTMLProtocolHeader(numOfProducts, result, form, reslist):
    """
    @numOfProducts число изделий
    @result один из результатов (оттуда списывается модель и дата теста)
    @reslist - список результатов. Оттуда берём серийные номера

    Создаёт голову таблицы
    """

    strnumprs=""
    #for x in range (1, numOfProducts+1):
     #   strnumprs+="<td align=center >{0}</td>\n".format(x)
    for x in reslist:
        strnumprs+="<td align=center >{0}</td>\n".format(sortResultsBySerial(x))


    res=""


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





def outreport (reslist, form, protocol, name=None):
    """

    name - имя набора параметров отчёта (из протокола)
    """
    return generateHTML (reslist, protocol, form, name), ""

    #bck.getProtocolFromDatabaseParams (ProductName, TestName)





def outreportsgroup (residlist, form, name):
    """
    residlist - список айди результатов
    form - дескриптор принятых параметрво формы
    name - имя набора парметров отчёта
    """
    residlist.sort()

    res=str()
    err=str()

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



    step=int(form.getfirst("field_step", ""))
    now = datetime.datetime.now()
    typeofthetest=form.getfirst("field_testtype", "")
    field_repformnumber = form.getfirst("field_repformnumber", "")


    res="<div align='center'> <p>ПРОТОКОЛ №{0} от {1}</p>".format (field_repformnumber, now.strftime("%Y-%m-%d"))



    #res="<div align='center'> <p>ПРОТОКОЛ №   от "+now.strftime("%Y-%m-%d")+"</p>  "


    res+="<p>"+typeofthetest+"</p>"
    res+="<p>"+result.model+"</p>"




    for i in range (0, len(reslist), step):
        outr=outreport(reslist[i:i+step], form, protocol, name)
        res+=outr[0]+"<br style='page-break-after: always'> "

    res+=generateOneReportFooter (form, reslist)

    return res + err




htmg.out (htmg.generateHTMLMetaHeader("Вывод отчётной формы", 0))
#получение списка результатов для построения отчётов
form = cgi.FieldStorage()

name=""
if "name" in form:
    name=form.getfirst("name", "")


residlist=list()
#making results list:
for key in form:
    #htmg.out(key+"  "+ form.getfirst(key, "")   +"</br>")
    if "checkbox" in key:
        residlist.append(int(key.split("_")[1]))

if len(residlist)>0:
    htmg.out(outreportsgroup(residlist, form, name))  #если список не пуст, вывести группу отчётов




htmg.out( htmg.generateHTMLFooter())


#Как ставить номер протокола? Добавить поля вид протокола (ОТК), вид испытаний (Предъявительские)
#Дату надо парсить в нормальный формат
#http://dik123.blogspot.ru/2009/02/html-pdf.html
#На этой странице написано, как переводить html-документы в pdf
