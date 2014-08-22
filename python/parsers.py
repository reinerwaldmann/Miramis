#!/usr/bin/python3.4
#!C:\Python33\python.exe

#-*- coding: utf-8
from itertools import starmap

__author__ = 'vasilev_is'
from classes import *
import datetime as dt
import dateutil.parser as dparser
import copy



def parseToResultCP1251 (filename):
    """
    Парсит файл filename в AResult
    """
    msg="" #сообщение, цепляемое к результату

    try:
        file=open(filename, "rb")
    except:
        print("Error while opening file")
        return None
    res=AResult()
    first_line=file.readline().decode("cp1251")
    if first_line.__contains__("ИВЭП")!=1:
        print ("Эта версия только для ИВЭП")
        exit(1)
    #парсим справочную часть
    for linex in file:
        line = linex.decode("cp1251")
        if line.__contains__("*"): # значит, дошли до главной части
            break

        linelst=line.strip().split(":")
        if linelst[0].__contains__("Модель"):
            res.model=linelst[1].strip()
        if linelst[0].__contains__("Имя программы"):
            res.typeOfTest=linelst[1].strip()
        if linelst[0].__contains__("Дата"):
            #res.testDateTime=linelst[1].strip()
            res.testDateTime=line[line.index(":")+1::].strip().replace("/", "-")
            #print (res.testDateTime)
            date=dparser.parse(res.testDateTime)
            #print(date)
            res.testDateTime = date.__str__()

        if linelst[0].__contains__("Контр"):
                res.operator=linelst[1].strip()
        if linelst[0].__contains__("Результат"):
                res.hasPassedTest=linelst[1].__contains__("PASS")
        if linelst[0].__contains__("Серийный номер"):
                res.numOfProduct = linelst[1].strip()
        if linelst[0].__contains__("Номер партии"):
               res.numOfBatch = linelst[1].strip()

    proclines=""
    for line in file:
        proclines+=line.decode("cp1251")

    #получили последовательность объектов resultsOfProcedure, применив парсинговую функцию
    ## ко всем строчкам, относившимся к результатам
    #срез потому, что иначе последним в сплите идёт пустая строка - ибо последняя процедура
    # в конце файла также имеет строчку из звёздочек с \n
    rrlist=proclines.split("********************************************************************************\r\n")[0:-1]
    rpcseq=list(map(parceToPrRes, rrlist))
    numseq=list(map (lambda  rpc: rpc.number, rpcseq))
    res.proceduresResults=dict(zip(numseq, rpcseq))
    return res




def parseToResult (filename):
    """
    Парсит файл filename в AResult
    """
    msg="" #сообщение, цепляемое к результату

    try:
        file=open(filename, "r")
    except:
        print("Error while opening file")
        return None
    res=AResult()
    first_line=file.readline()
    if first_line.__contains__("ИВЭП")!=1:
        print ("Эта версия только для ИВЭП")
        exit(1)
    #парсим справочную часть
    for line in file:
        if line.__contains__("*"): # значит, дошли до главной части
            break

        linelst=line.strip().split(":")
        if linelst[0].__contains__("Модель"):
            res.model=linelst[1].strip()
        if linelst[0].__contains__("Имя программы"):
            res.typeOfTest=linelst[1].strip()
        if linelst[0].__contains__("Дата"):


            #res.testDateTime=linelst[1].strip()
            res.testDateTime=line[line.index(":")+1::].strip().replace("/", "-")

            #print (res.testDateTime)
            date=dparser.parse(res.testDateTime)
            #print(date)

            res.testDateTime = date.__str__()




        if linelst[0].__contains__("Контр"):
                res.operator=linelst[1].strip()
        if linelst[0].__contains__("Результат"):
                res.hasPassedTest=linelst[1].__contains__("PASS")
        if linelst[0].__contains__("Серийный номер"):
                res.numOfProduct = linelst[1].strip()
        if linelst[0].__contains__("Номер партии"):
               res.numOfBatch = linelst[1].strip()

    proclines=""
    for line in file:
        proclines+=line

    #получили последовательность объектов resultsOfProcedure, применив парсинговую функцию
    ## ко всем строчкам, относившимся к результатам
    #срез потому, что иначе последним в сплите идёт пустая строка - ибо последняя процедура
    # в конце файла также имеет строчку из звёздочек с \n
    rrlist=proclines.split("********************************************************************************\n")[0:-1]
    rpcseq=list(map(parceToPrRes, rrlist))
    numseq=list(map (lambda  rpc: rpc.number, rpcseq))
    res.proceduresResults=dict(zip(numseq, rpcseq))
    return res


def parceToPrRes (line):
    """
    Парсит строку в результат  процедуры
    """
    rp=resultsOfProcedure()
    listlines=line.split("\n")
    rp.hasPassedProcedure=listlines[0].__contains__("PASS")

    # print (listlines[0])
    # return rp;
    rp.number=int(listlines[0].split(":")[0].split(".")[1])
    #или же поудалять все символы, которые не цифры




    strWithTables = line[line.rfind("Результаты измерений"):]  #строка, в которой находятся таблицы с результатами (возможно, одна  таблица)


    if "\n\r\n" in strWithTables : #если оная таблица содержит в себе пустую строку
    #if detector_two_tables:
        #Если в ней есть пустая строка, то считать случай 3 - есть и поканальный, и общий режимы
        #TODO но пока не  реализовно защиты от случайно впиленной пустой строки в конце, или чего-то подобного
        twotableslist = strWithTables.split("\n\r\n")

         #Здесь запилить парсинг общей таблицы

        comtable =twotableslist[0][twotableslist[0].find('\n')+1::  ]+"\n" #таблица с общими результатами

        rp.values_common = parseTable(comtable,"rescom") #распарсили результаты общие
        rp.values1 = parseTable(twotableslist[1],'res') #распарсили результаты поканальные



    else:
        if "Выходной канал" in strWithTables: #если данные только поканальные
            #Получили строку результатов измерений, и распарсили ей, считав только нормативы
            rp.values1 = parseTable(line[line.rfind("Результаты измерений"):],'res') #распарсили результаты поканальные

        else: #если есть только общие данные
            rp.values_common = parseTable(strWithTables,"rescom") #распарсили результаты общие



    #в этом месте пытается найти результаты измерений
    # ind=0
    # for i in range (0, listlines.__len__()):
    #     if (listlines[i].__contains__("Результаты измерений")):
    #         ind=i
    #         break
    # ind+=2
    # #print (listlines[ind])
    # value_names=listlines[ind][0: listlines[ind].rfind("#")].split("$")[1::]
    # ind+=2
    # rp.values1 = parseTable(line[line.rfind("Результаты измерений"):],'res')
    return rp


#на вход принимает таблицу
  # --------------------------
  # Выходной канал ИВЭП $ Iвых, А
  # -------------------  -------
  # 1 канал +5 В        $   3.000
#На выходе словарь словарей - имя канала - название параметра - значение

def parseTable (line, type):
    """
    Парсит таблицу во что прикажут: type: 'res' - если нужны результаты 'norm' - если нужны нормы 'mode' - если нужны режимы
    """
    line = line [line.find("-"):]
    listlines=line.split("\n")
    ind=1
    namesline=listlines[ind]

    #эта конструкция - аналог switch
    value_names = { #названия значений
    'res': lambda namesline: namesline[0: namesline.rfind("#")].split("$")[1::], #вариант для результатов
    'rescom': lambda namesline: namesline[0: namesline.rfind("#")].split("$"), #вариант для результатов

    'norm': lambda namesline: namesline[namesline.rfind("#")+1:].strip().split("$"), #вариант для норм
    'normcom': lambda namesline: namesline[namesline.rfind("#")+1:].strip().split("$"), #вариант для норм общих

    'mode': lambda namesline: namesline.split("$")[1::] #вариант для режима измерения

    #norm и normcom совпадают!
    }[type](namesline)



 # print (listlines[ind][listlines[ind].rfind("#"):].split("$")) #вариант для норм
    ind+=2
    rp=dict()
    while (ind!=listlines.__len__()-1): #цикл по строчкам каналов

        listnamesvals = {
            'res': lambda resline: resline[0: resline.rfind("#")].split("$"),
            'rescom': lambda resline: resline[0: resline.rfind("#")].split("$"),
            'norm': lambda resline: resline[resline.rfind("#")+1:].split("$"),
            'normcom': lambda resline: resline[resline.rfind("#")+1:].split("$"),
            'mode': lambda resline: resline.split("$")
        }[type](listlines[ind])


        channame=listlines[ind] [0: listlines[ind].rfind("#")].split("$")[0].strip()
        listvals= {
            'res' : listnamesvals[1::],
            'rescom' : listnamesvals,
            'norm': listnamesvals,
            'normcom': listnamesvals,
            'mode': listnamesvals[1::]
        }[type]



#ПИТОН - САМЫЙ ОМСКИЙ ЯЗЫК ВСЕХ ВРЕМЁН И НАРОДОВ!!! ЛЯМБДЫ ВО ВСЕ ПОЛЯ!!!!!!!!!!!
        valsdict=dict(zip(value_names, map (lambda d: d.strip(), listvals)))
        #valsdict=dict(zip(value_names, listvals))


        if "rescom" in type: #если считываем общие результаты, слить первую строчку сразу
            return valsdict

        if "normcom" in type:
            return valsdict


        rp[channame]=valsdict
        ind+=1
        #print (rp.number)
    return rp


def parseToProcedures (line):
    """
    Парсит в класс Procedures
    """
    rtp=Procedures ()

    #пилим на строки
    listlines=line.split("\n")

    #Получили номер процедуры
    rtp.number=int(listlines[0].split(":")[0].split(".")[1])

    #Получили имя процедуры
    rtp.name=listlines[1]

    #Получили строку режимов по каналам
    linemodetable = line[line.rfind("Режим измерения"):line.rfind("* Результаты измерений")]
    linemodetable = linemodetable[linemodetable.find("--"):-1]
    rtp.mode_channel = parseTable(linemodetable,'mode')

    strWithTables = line[line.rfind("Результаты измерений"):]  #строка, в которой находятся таблицы с результатами (возможно, одна  таблица)


    if "\n\n" in strWithTables : #если оная таблица содержит в себе пустую строку
    #if detector_two_tables:
        #Если в ней есть пустая строка, то считать случай 3 - есть и поканальный, и общий режимы
        #TODO но пока не  реализовно защиты от случайно впиленной пустой строки в конце, или чего-то подобного
        twotableslist = strWithTables.split("\n\n")

         #Здесь запилить парсинг общей таблицы

        print (rtp.number)

        comtable =twotableslist[0][twotableslist[0].find('\n')+1::  ]+"\n"
        rtp.normal_values_common = parseTable(comtable,"normcom") #распарсили нормы общие
        rtp.listOfPossibleResultsCommon = list (parseTable(comtable,"rescom").keys()) #распарсили результаты общие
        rtp.normal_values = parseTable(twotableslist[1],'norm') #распарсили нормы поканальные
        rtp.listOfPossibleResults = list( list ( parseTable(twotableslist[1],'res').values())[0].keys()) #распарсили результаты поканальные

    else:
        if "Выходной канал" in strWithTables: #если данные только поканальные
            #Получили строку результатов измерений, и распарсили ей, считав только нормативы
            rtp.normal_values = parseTable(line[line.rfind("Результаты измерений"):],'norm')
            #Получаем  строку названий возможных результатов
            possibleResults = list ( parseTable(line[line.rfind("Результаты измерений"):],'res').values()  )
            rtp.listOfPossibleResults=list(  possibleResults[0].keys())

        else: #если есть только общие данные
            rtp.normal_values_common = parseTable(strWithTables,"normcom") #распарсили нормы общие
            rtp.listOfPossibleResultsCommon = list (parseTable(strWithTables,"rescom").keys()) #распарсили результаты общие


    #Получили строку режимов просто
    linecommonmode = line[line.find("Режим измерения"): line.find("--",line.find('Режим измерения')) ]
    listcommonmode=linecommonmode.split('\n')[1:-1]
    parsefunc = lambda s: list (map (lambda g: g.strip() , s.split ("=")))
    rtp.mode_common =  (dict(map (parsefunc, listcommonmode)))

    return rtp

def parseToAProtocol (file):
    """
    Парсит в класс AProtocol
    на входе - дескриптор файла
    """

    ap=AProtocol()
    first_line=file.readline()
    #if first_line.__contains__("ИВЭП")!=1:
    if not "ИВЭП" in first_line:
        print ("Эта версия только для ИВЭП")
        exit(1)
    #парсим справочную часть
    for line in file:
        if line.__contains__("*"): # значит, дошли до главной части
            break
        linelst=line.strip().split(":")
        if linelst[0].__contains__("Модель"):
            ap.model=linelst[1].strip()
        if linelst[0].__contains__("Имя программы"):
            ap.typeOfTest=linelst[1].strip()

    proclines=""
    for line in file:
        proclines+=line
    rrlist=proclines.split("********************************************************************************\n")[0:-1]

    rpcseq=list(map(parseToProcedures, rrlist))
    numseq=list(map (lambda  app: app.number, rpcseq))
    ap.procedures=dict(zip(numseq, rpcseq))

    #print   (ap.procedures.items().)

    ap.channelname=list(rpcseq[0].mode_channel.keys())

#    print (ap)

    return ap
def parseToAProtocolCP1251(file):
    """
    Парсит в класс AProtocol, если входной файл записан в CP1251
    на входе - дескриптор файла
    """
    try:

        ap=AProtocol()
        first_line=file.readline().decode("cp1251")
        if first_line.__contains__("ИВЭП")!=1:
            return None, "Эта версия только для ИВЭП"
        #парсим справочную часть
        for linex in file:
            line = linex.decode("cp1251")[:-2]+"\n"
            if line.__contains__("*"): # значит, дошли до главной части
                break
            linelst=line.strip().split(":")
            if linelst[0].__contains__("Модель"):
                ap.model=linelst[1].strip()
            if linelst[0].__contains__("Имя программы"):
                ap.typeOfTest=linelst[1].strip()

        proclines=""
        for linex in file:
            line = linex.decode("cp1251")[:-2]+"\n"
            proclines+=line


        rrlist=proclines.split("********************************************************************************\n")[0:-1]


        rpcseq=list(map(parseToProcedures, rrlist))
        numseq=list(map (lambda  app: app.number, rpcseq))
        ap.procedures=dict(zip(numseq, rpcseq))

        #print   (ap.procedures.items().)
        try:
        #    ap.channelname=list(rpcseq[0].mode_channel.keys())
            ap.channelname=list(rpcseq[0].mode_channel.keys())


        except BaseException:
            ap.channelname=list()

    except BaseException as e:
        return None, "Some error occured"


    return ap, ""
def parseToAProtocolStr (instr):
    """
    Парсит в класс AProtocol
    на входе - дескриптор файла
    """

    instr.split("\n")

    ap=AProtocol()
    first_line=file.readline()
    #if first_line.__contains__("ИВЭП")!=1:
    if not "ИВЭП" in first_line:
        print ("Эта версия только для ИВЭП")
        exit(1)
    #парсим справочную часть
    for line in file:
        if line.__contains__("*"): # значит, дошли до главной части
            break
        linelst=line.strip().split(":")
        if linelst[0].__contains__("Модель"):
            ap.model=linelst[1].strip()
        if linelst[0].__contains__("Имя программы"):
            ap.typeOfTest=linelst[1].strip()

    proclines=""
    for line in file:
        proclines+=line
    rrlist=proclines.split("********************************************************************************\n")[0:-1]
    rpcseq=list(map(parseToProcedures, rrlist))
    numseq=list(map (lambda  app: app.number, rpcseq))
    ap.procedures=dict(zip(numseq, rpcseq))

    #print   (ap.procedures.items().)

    #ap.channelname=list(rpcseq[0].mode_channel.keys())

    try:
        ap.channelname=list(rpcseq[0].mode_channel.keys())
    except BaseException:
        ap.channelname=list()


#    print (ap)

    return ap




#Такая структура, как представлена, даёт возможность генерировать также и пустые объекты для  заполнения их руками
#Заполненность объектов может быть любой, от никакой вообще (пустой объект) и до полной.



#TODO привести перекодиование в порядок, когда дело дойдёт до загрузки


# import platform
# #print (platform.system())
#
# if (platform.system().__contains__("Linux")):
#     filename="utf8.txt" #и вот тут должно быть перекодирование, тащемта
# else:
#     filename="protocolCP1251.txt"




#тестовая хрень

def test ():
    #filename="G:\\Projects\\Miramis\\MiramisNewest\\Miramis\\Materials\\NewProtocols\\1б.txt"

    #f = open ("G:\\Projects\\Miramis\\MiramisNewest\\Miramis\\Materials\\NewProtocols\\nocommon1.txt", "rt")
    filename = "G:\\Projects\\Miramis\\MiramisNewest\\Miramis\\Materials\\NewProtocols\\nocommon1.txt"

    #f = open (filename)
#    print (parseToAProtocol(f).procedures[9].__str__())

    print (parseToResult(filename).proceduresResults[8].toHTML())






#test()



