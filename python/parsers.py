#!/usr/bin/python3.4
#!/usr/bin/python3.4
#!C:\Python33\python.exe

#-*- coding: utf-8


__author__ = 'vasilev_is'
from classes import *
import dateutil.parser as dparser


#service functions
def searchFirstLineInList (lst, str, contains=True):
#возвращает индекс первой строки с начала списка, в которой найдена str
    for i in range (len(lst)):
        if str in lst[i] and contains:#содержать
            return i
        if not contains and str==lst[i]: #равняться
            return i

    return -1
def stripLineList (listlines1):
    while listlines1[0]=='':
        del (listlines1[0])

    while listlines1[len(listlines1)-1]=='':
        listlines1.pop()

        #listlines1.remove(listlines1[len(listlines1)-1])


#на вход принимает таблицу
  # --------------------------
  # Выходной канал ИВЭП $ Iвых, А
  # -------------------  -------
  # 1 канал +5 В        $   3.000
def parseTable (line, type):
    """
    Парсит таблицу во что прикажут: type: 'res' - если нужны результаты 'norm' - если нужны нормы 'mode' - если нужны режимы
    """
    #На выходе словарь словарей - имя канала - название параметра - значение
    line = line [line.find("-"):]   #для результата для v2 это не делает ничего, ибо там уже начинается с палки
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
    #while (ind!=listlines.__len__()-1): #цикл по строчкам каналов
    while ind<len(listlines) and  ( listlines[ind].strip()!='')   :

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
def delcomments (line):
    listlines=line.split("\n")
    listToPop=list()

    for i in range (0, len(listlines)-1):

        try:
            while listlines[i].strip()[0]=="/":
         #       print (listlines[i])
                listlines.pop(i)
                #listToPop.append (i)

        except BaseException:
            pass

    # reslist=list()
    # for i in range (0, len(listlines)-1):
    #     if not i in listToPop:
    #         reslist.append(listlines[i])

    return "\n".join(listlines)

#basic parse functions
def basicParserTextForm (file, type='result'):
    """формирует и протокол, и результат. А выдаёт то, что затребовано
    эту процедуру потом можно оборачивать для совместимости во всякое"""

    msg="" #сообщение, цепляемое к результату

    res=AResult()
    prot=AProtocol()

    first_line=file.readline()
    if first_line.__contains__("ИВЭП")!=1:
        raise RuntimeError ('basicParserTextForm: Текстовый файл не имеет префикса ИВЭП, а эта версия рассчитана только на работу с ИВЭП.') #в данном варианте мы ничего не возвращаем, а просто выбрасываем исключение.
        #код выше по уровню будет обрабатывать исключения. Таким образом, он обработает как выброшенные нами исключения, вроде этого, так и встроенные, которые тоже могут появиться


    try:
        #парсим справочную часть
        for line in file:
            if line.__contains__("*"): # значит, дошли до главной части
                break
            linelst=line.strip().split(":")
            if linelst[0].__contains__("Модель"):
                prot.model=res.model=linelst[1].strip()
            if linelst[0].__contains__("Имя программы"):
                prot.typeOfTest=res.typeOfTest=linelst[1].strip()
            if linelst[0].__contains__("Дата"):
                #res.testDateTime=linelst[1].strip()
                res.testDateTime=line[line.index(":")+1::].strip().replace("/", "-")
                #print (res.testDateTime)
                date=dparser.parse(res.testDateTime)
                #print(date)
                res.testDateTime = date.date().isoformat()
            if linelst[0].__contains__("Контр"):
                    res.operator=linelst[1].strip()
            if linelst[0].__contains__("Результат"):
                    res.hasPassedTest=linelst[1].__contains__("PASS")
            if linelst[0].__contains__("Серийный номер"):
                    res.numOfProduct = linelst[1].strip()
            if linelst[0].__contains__("Номер партии"):
                   res.numOfBatch = linelst[1].strip()

    except Exception as e: #если случилось хотя бы что либо при парсинге этой части
        e.args = (e.args[0] + ' basicParserTextForm: Ошибка в парсинге справочной части.',) #добавляем к описанию ошибки свой текст
        raise #пропускаем исключение дальше


    try:
        proclines=""
        for line in file:
            proclines+=line
        #FIXME сама идея сначала резать файл на список, а потом опять собирать его в строку, да ещё и так криво потом разбирать на процидурки - кажется кривой, но поделать нечего
        #срез потому, что иначе последним в сплите идёт пустая строка - ибо последняя процедура
        # в конце файла также имеет строчку из звёздочек с \n
        rrlist=proclines.split("********************************************************************************\n")[0:-1]
    except Exception as e:
        e.args = (e.args[0] + ' basicParserTextForm: Ошибка при объединении на строчки и распиле на процедуры.',) #добавляем к описанию ошибки свой текст
        raise #пропускаем исключение дальше



    try:
        reslist=list(map(basicParserTextProcedure, rrlist)) #список результатов процедур
    except Exception as e:
        e.args = (e.args[0] + ' basicParserTextForm: Ошибка при формирование списка результатов процедур.',) #добавляем к описанию ошибки свой текст
        #raise RuntimeError (' basicParserTextForm: Ошибка при формирование списка результатов процедур.') from e
        raise
        #e.args = (e.args[0] + ' basicParserTextForm: Ошибка при формирование списка результатов процедур.',) #добавляем к описанию ошибки свой текст
        #raise #пропускаем исключение дальше

    try:
        proclist=list(map(lambda x: basicParserTextProcedure(x, 'protocol'), rrlist)) #список результатов процедур
    except Exception as e:

        #raise RuntimeError (' basicParserTextForm: Ошибка при формирование списка процедур.') from e
        e.args = (e.args[0] + ' basicParserTextForm: Ошибка при формирование списка процедур.',) #добавляем к описанию ошибки свой текст
        raise #пропускаем исключение дальше


    numseq=list(map (lambda  rpc: rpc.number, reslist))

    res.proceduresResults=dict(zip(numseq, reslist))
    prot.procedures=dict(zip(numseq, proclist))

    prot.channelname=list(proclist[0].mode_channel.keys())

    if type=='result':
        return res
    elif type=='protocol':
        return prot
    else:
        raise RuntimeError('basicParserTextForm: Некорректное задание типа выходного объекта')
def basicParserTextProcedure (line, type='result'):
#формирует процедуру и для протокола, и для результата
    """
    Парсит строку в результат  процедуры
    """
    line = delcomments(line)

    rp=resultsOfProcedure()#результат процедуры
    pp=Procedures() #процедура

    linemodetable = line[line.rfind("Режим измерения"):line.rfind("* Результаты измерений")]
    linemodetable = linemodetable[linemodetable.find("--"):-1]
    pp.mode_channel = parseTable(linemodetable,'mode')

     #Получили строку режимов просто
    linecommonmode = line[line.find("Режим измерения"): line.find("--",line.find('Режим измерения')) ]
    listcommonmode=linecommonmode.split('\n')[1:-1]
    parsefunc = lambda s: list (map (lambda g: g.strip() , s.split ("=")))
    pp.mode_common = (dict(map (parsefunc, listcommonmode)))





    listlines=line.split("\n")
    listlines1=[x.strip() for x in line.split("\n")] #создали список строк, у каждой из которой выпилены spance, \r\n и прочее

    rp.hasPassedProcedure=listlines1[0].__contains__("PASS")
    pp.number=rp.number=int(listlines1[0].split(":")[0].split(".")[1])

    pp.name = listlines1[1]


    try:

        listOfStrsWithTables = listlines1[searchFirstLineInList(listlines1, 'Результаты измерений'):]  #слайс списка, начиная с требуемого нам индекса
        stripLineList(listOfStrsWithTables)
        strWithTables = line[line.rfind("Результаты измерений"):]  #строка, в которой находятся таблицы с результатами (возможно, одна  таблица)
        splitinddex = searchFirstLineInList(listOfStrsWithTables, '', contains=False)

        if splitinddex!=-1 and splitinddex!=len(listOfStrsWithTables)-1 and splitinddex!=0: #если  есть и общие и поканальные
        #if splitinddex !=all((-1,len(listOfStrsWithTables)-1,0)):
        #если процедура поиска не выдала -1, тоесть отсутствие пустых строк, последний элемент, то есть пустую строку в конце, 0, то есть её же в начале
            commonpart = listOfStrsWithTables[1:splitinddex] #отсекаем "результаты измерений"
            channelpart = listOfStrsWithTables[splitinddex+1:]

            comtablestr = '\n'.join(commonpart) #костыль для объединения списка в няшную строку для скармливания таблицепарсеру
            chtablestr = '\n'.join(channelpart) #костыль для объединения списка в няшную строку для скармливания таблицепарсеру

            rp.values_common = parseTable(comtablestr,'rescom') #распарсили результаты общие
            rp.values1 = parseTable(chtablestr,'res') #распарсили результаты поканальные

            #pp.listOfPossibleResultsCommon = list (parseTable(comtablestr,"rescom").keys()) #распарсили результаты общие
            pp.listOfPossibleResultsCommon = list(list (rp.values_common.keys())) #распарсили результаты общие

            #pp.listOfPossibleResults = list( list ( parseTable(twotableslist[1],'res').values())[0].keys()) #распарсили результаты поканальные
            pp.listOfPossibleResults = list(list(rp.values1.values())[0].keys())

            pp.normal_values = parseTable(chtablestr,'norm') #распарсили нормы поканальные
            pp.normal_values_common = parseTable(comtablestr,"normcom") #распарсили нормы общие

        else:
            if "Выходной канал" in strWithTables: #если данные только поканальные
                #Получили строку результатов измерений, и распарсили ей, считав только нормативы
                rp.values1 = parseTable(line[line.rfind("Результаты измерений"):],'res') #распарсили результаты поканальные
                pp.listOfPossibleResults = list(list(rp.values1.values())[0].keys())

                pp.normal_values = parseTable(line[line.rfind("Результаты измерений"):],'norm') #распарсили нормы поканальные


            else: #если есть только общие данные
                rp.values_common = parseTable(strWithTables,"rescom") #распарсили результаты общие
                pp.listOfPossibleResultsCommon = list (rp.values_common.keys()) #распарсили результаты общие

                pp.normal_values_common = parseTable(strWithTables,"normcom") #распарсили нормы общие


    except Exception as e:
         e.args = (e.args[0] + 'We got an error in procedure number {0}'.format (rp.number),) #добавляем к описанию ошибки свой текст
         raise e


         #raise RuntimeError('We got an error in procedure number {0}'.format (rp.number)) from e #это тоже вариант, тогда будет выброшено два исключения - Runtime и e, притом e будет названо
        # прямой причиной Runtime
        # то есть, скажем, исключение в анализе файла выбрасываем и говорим, что оно есть следствие исключения в анализе процедуры

    if type=='result':
        return rp
    elif type=='protocol':
        return pp
    else:
        raise RuntimeError('basicParserTextProcedure Некорректное задание типа выходного объекта')


def basicParserTextFormFilename (filename, type='result'):
    try:
        with open(filename, "rt",  encoding='cp1251') as file:
            try:
                return basicParserTextForm (file, type),''
            except BaseException as e:
                return None, e.__str__()+str(e.__traceback__)
    except BaseException:
        return None, e.__str__()+str(e.__traceback__)

#wrapper functions
def parseToResult (filename):
    """
    Парсит файл filename в AResult
    """
    #FIXME надлежит посмотреть на верхних уровнях, как передать суть заключения туда, и затем вписать в логи, что ли
    msg="" #сообщение, цепляемое к результату

    try:
        with open(filename, "rt",  encoding='cp1251') as file:
            try:
                return basicParserTextForm (file)
            except BaseException as e:
                return None
    except BaseException:
        return None

def parseToAProtocolCP1251(file):
    """
    Парсит в класс AProtocol, если входной файл записан в CP1251
    на входе - дескриптор файла
    """
    #эта хрень не работает!!!


    try:
        return basicParserTextForm (file, type='protocol'), ""
    except BaseException as e:
        return None, e.__str__()+str(e.__traceback__)








