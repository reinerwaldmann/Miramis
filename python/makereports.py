#!/usr/bin/python3.4
#!/usr/bin/python3.4
#!/usr/bin/python3.4
#!/usr/bin/python3.4
#!/usr/bin/python3.4
__author__ = 'vasilev_is'

from classes import *
from  htmlgeneralfunctions import *


"""
Файл, занимающийся производством отчётов
"""

#[FRONTEND]

#начинаем создавать хытымыль-страницу
#хытымыль страница состоит из шапки и главной части по одной классификации
#и из программы испытаний и протокола испытаний по другой классификации
#главная часть состоит из процедур, каждая из которых генерируется отдельно
#каждая процедура состоит из левой и правой части. Левая часть заполняется из программы испытаний, правая часть заполняется из протокола испытаний


def generateHTML (resultslist:list, protocol:AProtocol):
    """
    @resultslist список результатов
    @protocol протокол

    Генерирует тело таблицы
    """
    if (resultslist == None):
        throwError("makereports", "Ошибка, None как список резльутатов")
        return ""

    if (protocol == None):
        throwError("makereports", "Ошибка, None как протокол")
        return ""

    if (resultslist.__len__==0):
        throwError("makereports", "Нет результатов в списке!")
        return ""


    res=generateHTMLMetaHeader() + generageHTMLProtocolHeader(resultslist.__len__(), resultslist[0])
    #res+=generageHTMLProtocolHeader(resultslist[0])  #resultslist - это список результатов. Результатов всегда список, тогда как протокол - один
    #таблица пошла

    #Здесь можно напистаьпроверку на соответствие результатов протоколу

    for i in (1,protocol.procedures.__len__()):
        p=protocol.procedures[i]
        res+="<tr>"+p.toHTML()
        for k in resultslist:
            res+="<td>{0}</td>".format(k.proceduresResults[p.number].toHTML())
        res+="</tr>"
        #res+= """<tr> {0} <td> </td> <td> </td> <td> </td> </tr> """.format(p.toHTML())


    res += generateHTMLFooterRep()
    return res



def generageHTMLProtocolHeader(numOfProducts, result):
    """
    @numOfProducts число изделий
    @result один из результатов (оттуда списывается модель и дата теста)
    Создаёт голову таблицы
    """
    res="<div align='center'> <p>ПРОТОКОЛ №  от "+result.testDateTime+"</p>  "
    res+="<p> Каких-то испытаний, установить!!</p>"
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


#Как ставить номер протокола? Добавить поля вид протокола (ОТК), вид испытаний (Предъявительские)
#Дату надо парсить в нормальный формат


#для отладки создаём хтмль файл



#as file opened in binary, we can write there encoded bytes sequence, cyrillic one this case

#http://dik123.blogspot.ru/2009/02/html-pdf.html
#На этой странице написано, как переводить html-документы в pdf

#Перекодирование файла в папке в utf8
#Это же можно делать и построчно, во время чтения

#f = file("utf8.html", "wb")
#for line in file("cp1251.html", "rb"):
#    f.write(line.decode('cp1251').encode('utf8'))

#commented, uncomment if original file in CP1251 changed
#text_in_cp1251 = open("sandbox/protocolCP1251.txt", 'rb').read()
#text_in_unicode = text_in_cp1251.decode('cp1251')
#text_in_utf8 = text_in_unicode.encode('utf8')
#open('sandbox/utf8.txt', 'wb').write(text_in_utf8)
#parseToResult ("sandbox/protocolCP1251.txt")
#print (parseToAProtocol("sandbox/protocolCP1251.txt"))


#TODO   1. Рефакторинг кода
#TODO   3. Тестирование создания HTML-странички и добавление дополнительных полей вроде вида испытаний (возможно, их вводить при генерации)
#TODO   4. Проектирование веб-страницы с полями ввода и так далее




#wb-binary mode,
# htmlfile = open("index.html", "wb")
#htmlfile.write (generateHTML( (parseToResult("sandbox/"+filename), parseToResult("sandbox/"+filename), parseToResult("sandbox/"+filename) ) , parseToAProtocol( "sandbox/"+filename  )  ).encode("utf-8"))
# result = parseToResult ("sandbox/"+filename)
# protocol = parseToAProtocol("sandbox/"+filename)






