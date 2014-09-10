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
import cgitb, cgi, io, sys, os
#cgitb.enable()

"""
Данный скрипт делает групповые отчёты и выводит их в html формате
(пока так, потом, возможно, в зависимости от настроек, и в pdf)

"""

isdebug=0

def closeAsError (errmsg):
    global isdebug
    if isdebug:
        htmg.out (errmsg)
    htmg.out(list().__str__())
    exit(0)




#начинаем создавать хытымыль-страницу
#хытымыль страница состоит из шапки и главной части по одной классификации
#и из программы испытаний и протокола испытаний по другой классификации
#главная часть состоит из процедур, каждая из которых генерируется отдельно
#каждая процедура состоит из левой и правой части. Левая часть заполняется из программы испытаний, правая часть заполняется из протокола испытаний


htmg.out (htmg.generateSimpleMetaHeader())

#получение списка результатов для построения отчётов
form = cgi.FieldStorage()
residlist=list()
#making results list:

errlog = ""

if "debug" in form:
    isdebug=1
    htmg.out ("Hello, debug mode!")
    


for key in form:
    #htmg.out(key+"  "+ form.getfirst(key, "")   +"</br>")
    if "checkbox" in key:
        residlist.append(int(key.split("_")[1]))

if len(residlist)==0:
    #если список пуст - выйти
    closeAsError ("Ошибка: список пуст")

reslist=list()
for resid in residlist:
    res = bmr.getResultFromDatabase(resid)  # Получить результат из базы данных
    if res[0]==None:
        errlog+="Ошибка: такого результата нет в базе данных"
    else:
        reslist.append(res[0])

if len(reslist)==0: #если список результатов пуст, это из-за всяких ошибок может быть
    closeAsError ("Список результатов пуст")

for result in reslist: #проверяем список результатов на однородность, то есть все результаты должны быть от одного протокола
    if not result.model==reslist[0].model or not result.typeOfTest==reslist[0].typeOfTest:

        closeAsError ("Ошибка: в выборке присутствуют результаты от разных протоколов")
prot = bck.getProtocolFromDatabaseParams (reslist[0].model, reslist[0].typeOfTest)
if prot[0]==None:
     closeAsError("Ошибка: в базе данных нет протокола под такой результат")


protocol=prot[0]

if not protocol.dictOfReportFormParameters:
    closeAsError("Список возможных параметров отчётов у данного протокола совершенно пуст")


htmg.out(list(protocol.dictOfReportFormParameters.keys()).__str__())






exit(0)










#Как ставить номер протокола? Добавить поля вид протокола (ОТК), вид испытаний (Предъявительские)
#Дату надо парсить в нормальный формат
#http://dik123.blogspot.ru/2009/02/html-pdf.html
#На этой странице написано, как переводить html-документы в pdf
