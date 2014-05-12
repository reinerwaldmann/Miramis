import datetime
from datetime import datetime
from idlelib import rpc


class BaseStrReturn:
    def __str__(self):
        res="["+type(self).__name__+"]\n"
        for line, value in self.__dict__.items():
            res+=line+":\t"+value.__str__()+"\n"
        return res

#Класс, представляющий тип протокола (т. е. тип изделие - испытания)
class AProtocol(BaseStrReturn):
    model=str()
    typeOfTest=str()
    channelname=list()
    procedures=dict()
    def __str__(self):
        res=BaseStrReturn.__str__(self)
        for key, val in self.procedures.items():
            res+=str(key)+" : "+val.__str__().replace("\n", "\n\t")   #выводим с отступом
        return res


    #     res+="\n"+self.typeOfTest
    #     res+="\n"+self.channelname
    #     res+="\n"+self.procedures
    #     return res

#Класс, представляющий процедуру из типа протокола
class Procedures(BaseStrReturn):
    number=int() #номер порядковый
    name=""  #имя процедуры
    mode_common=dict() #словарь общих режимов имя-значение
    mode_channel=dict(dict()) #словарь словарей режимов по каналам (имя канала - имя параметра - значение)
    normal_values=dict(dict()) #словарь словарей значений нормативов название канала-название параметра-строка больше-меньше (значение параметра)



#Представляет один результат
class AResult (BaseStrReturn):
    model=str()
    typeOfTest=str()
    operator=str()
    testDateTime=str()
    testTime=str()
    numOfProduct=int()
    numOfBatch=int()
    hasPassedTest=bool() #1 - прошёл, 0 - не прошйл. Результаты испытаний
    proceduresResults=dict() #номер испытания - resultsOfProcedure
    def __str__(self):
        res=BaseStrReturn.__str__(self)
        for key, val in self.proceduresResults.items():
            res+=str(key)+" : "+val.__str__().replace("\n", "\n\t")   #выводим с отступом


        return res

        #res=self.model
       # res+="\n"+self.typeOfTest

       # print (self.testDate.__str__())
        #print (self.testTime.__str__())
        #print (self.numOfProduct.__str__())
        #print (self.numOfBatch.__str__())
        #print (self.hasPassedTest.__str__())
        #print (self.proceduresResults.__str__())
    #    return self.__dict__.__str__()



#Представляет результат процедуры
class resultsOfProcedure(BaseStrReturn):
    #парсит в resultsOfProcedure, каковой и возвращает.
    def __init__(self):
        number=int()
        hasPassedProcedure=bool()
        values1=dict()  #словарь словарей название канала - название параметра - значение


    #
    # def __init__(self, line):
    #     listlines=line.split("\n")
    #     self.hasPassedProcedure=listlines[0].__contains__("PASS")
    #
    #     # print (listlines[0])
    #     # return rp;
    #     self.number=int(listlines[0].split(":")[0].split(".")[1])
    #      #или же поудалять все символы, которые не цифры
    #     ind=0
    #     for i in range (0, listlines.__len__()):
    #         if (listlines[i].__contains__("Результаты измерений")):
    #             ind=i
    #             break
    #     ind+=2
    #     #print (listlines[ind])
    #     value_names=listlines[ind][0: listlines[ind].rfind("#")].split("|")[1::]
    #     #print (channel_names)
    #     ind+=2
    #
    #     #объединить операторы, парсящие таблицу, в функцию
    #     self.values1=dict()
    #     while (ind!=listlines.__len__()-1): #цикл по строчкам каналов
    #         #print (listlines[ind])
    #         listnamesvals=listlines[ind][0: listlines[ind].rfind("#")].split("|")
    #         channame=listnamesvals[0]
    #         listvals=listnamesvals[1::]
    #         valsdict=dict(zip(value_names, listvals))
    #         self.values1[channame]=valsdict
    #         ind+=1
    #         #print (rp.number)



    def __str__(self):
        res = BaseStrReturn.__str__(self)   #по непонятной причине, BaseStrReturn отказывается выводить словарь словарей
        return res



#Эта функция - ещё тестовая. Она будет впихивать данные из протокола в класс AResult
def parseToResult (filename):
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
            res.testDateTime=linelst[1].strip()
        if linelst[0].__contains__("Контр"):
                res.operator=linelst[1].strip()
        if linelst[0].__contains__("Результат"):
                res.hasPassedTest=linelst[1].__contains__("PASS")
        if linelst[0].__contains__("Серийный номер"):
                res.numOfProduct=linelst[1].strip()
        if linelst[0].__contains__("Номер партии"):
               res.numOfBatch=linelst[1].strip()

    proclines=""
    for line in file:
        #if line.__contains__("**"): # значит, дошли следующего шага
         #   break
        #procline+=line
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
        rp=resultsOfProcedure()
        listlines=line.split("\n")
        rp.hasPassedProcedure=listlines[0].__contains__("PASS")

        # print (listlines[0])
        # return rp;
        rp.number=int(listlines[0].split(":")[0].split(".")[1])
         #или же поудалять все символы, которые не цифры
        ind=0
        for i in range (0, listlines.__len__()):
            if (listlines[i].__contains__("Результаты измерений")):
                ind=i
                break
        ind+=2
        #print (listlines[ind])
        value_names=listlines[ind][0: listlines[ind].rfind("#")].split("|")[1::]
        ind+=2

        #объединить операторы, парсящие таблицу, в функцию

        # rp.values1=dict()
        # while (ind!=listlines.__len__()-1): #цикл по строчкам каналов
        #     #print (listlines[ind])
        #     listnamesvals=listlines[ind][0: listlines[ind].rfind("#")].split("|")
        #     channame=listnamesvals[0]
        #     listvals=listnamesvals[1::]
        #     valsdict=dict(zip(value_names, listvals))
        #     rp.values1[channame]=valsdict
        #     ind+=1
        #     #print (rp.number)

        rp.values1 = parseTable(line[line.rfind("Результаты измерений"):],'res')



        return rp


#на вход принимает таблицу
  # --------------------------
  # Выходной канал ИВЭП | Iвых, А
  # -------------------  -------
  # 1 канал +5 В        |   3.000
#На выходе словарь словарей - имя канала - название параметра - значение

def parseTable (line, type):
        line = line [line.find("-"):]
        listlines=line.split("\n")
        ind=1
        namesline=listlines[ind]
        value_names = {
        'res': lambda namesline: namesline[0: namesline.rfind("#")].split("|")[1::],       #вариант для результатов
        'norm': lambda namesline: namesline[namesline.rfind("#")+1:].strip().split("|"),  #вариант для норм
        'mode': lambda namesline: namesline.split("|")[1::] #вариант для режима измерения
        }[type](namesline)
     #   print (listlines[ind][listlines[ind].rfind("#"):].split("|"))  #вариант для норм
        ind+=2
        rp=dict()
        while (ind!=listlines.__len__()-1): #цикл по строчкам каналов
            listnamesvals = {
                'res': lambda resline: resline[0: resline.rfind("#")].split("|"),
                'norm': lambda resline: resline[resline.rfind("#")+1:].split("|"),
                'mode': lambda resline: resline.split("|")
            }[type](listlines[ind])
            channame=listlines[ind] [0: listlines[ind].rfind("#")].split("|")[0].strip()
            listvals= {
                'res' :  listnamesvals[1::],
                'norm':  listnamesvals,
                'mode': listnamesvals[1::]
            }[type]
#ПИТОН - САМЫЙ ОМСКИЙ ЯЗЫК ВСЕХ ВРЕМЁН И НАРОДОВ!!! ЛЯМБДЫ ВО ВСЕ ПОЛЯ!!!!!!!!!!!
            valsdict=dict(zip(value_names,   map (lambda d: d.strip(), listvals)))
            #valsdict=dict(zip(value_names, listvals))
            rp[channame]=valsdict
            ind+=1
            #print (rp.number)
        return rp




def parseToProcedures (line):
    rtp=Procedures ()
    listlines=line.split("\n")
    rtp.number=int(listlines[0].split(":")[0].split(".")[1])
    rtp.name=listlines[1]
    linemodetable=line[line.rfind("Режим измерения"):line.rfind("* Результаты измерений")]
    linemodetable =linemodetable[linemodetable.find("--"):-1]
    rtp.mode_channel = parseTable(linemodetable,'mode')
    rtp.normal_values= parseTable(line[line.rfind("Результаты измерений"):],'norm')

    linecommonmode = line[line.find("Режим измерения"): line.find("--",line.find('Режим измерения')) ]
    listcommonmode=linecommonmode.split('\n')[1:-1]
    parsefunc = lambda s: list (map (lambda g: g.strip() , s.split ("=")))
    rtp.mode_common =  (dict(map (parsefunc, listcommonmode)))
    return rtp

def parseToAProtocol (filename):
    try:
        file=open(filename, "r")
    except:
        print("Error while opening file")
        return None
    ap=AProtocol()
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


#Такая структура, как представлена, даёт возможность генерировать также и пустые объекты для  заполнения их руками
#Заполненность объектов может быть любой, от никакой вообще (пустой объект) и до полной.

#начинаем создавать хытымыль-страницу
#хытымыль страница состоит из шапки и главной части по одной классификации
#и из программы испытаний и протокола испытаний по другой классификации
#главная часть состоит из процедур, каждая из которых генерируется отдельно
#каждая процедура состоит из левой и правой части. Левая часть заполняется из программы испытаний, правая часть заполняется из протокола испытаний




result = parseToResult ("sandbox/protocolCP1251.txt")
protocol = parseToAProtocol("sandbox/protocolCP1251.txt")




def generateHTML (resultslist:list, protocol:AProtocol):
    if (resultslist.__len__()==0):
        return ""

    res=generateHTMLMetaHeader()
    res+=generageHTMLProtocolHeader(resultslist[0])  #resultslist - это список результатов. Результатов всегда список, тогда как протокол - один
    #таблица пошла


    res += generateHTMLFooter()
    return res


def generateHTMLResult (result):
    pass


#генерирует начало HTML-файла
def generateHTMLMetaHeader():
    res="""<!DOCTYPE html>
    <html lang="ru-RU">
    <head>
    <meta charset="UTF-8" />
    <title>Протокол испытаний</title>
    <link rel="stylesheet" type="text/css" media="all" href="" />
    </head>
    <body>
    """
    return res

def generageHTMLProtocolHeader(result):
    res="<p align='center'> ПРОТОКОЛ №  от "+result.testDate+"  </p>"
    res+="Каки-то испытаний, установить!!"
    res+="<p>"+result.model+"</p"
    return res



#Как ставить номер протокола? Добавить поля вид протокола (ОТК), вид испытаний (Предъявительские)
#Дату надо парсить в нормальный формат

def generateHTMLFooter():
    return """
    </body> </html>
    """
#добавить подпися, если надо

#для отладки создаём хтмль файл


#wb-binary mode,
htmlfile = open("index.html", "wb")
htmlfile.write (generateHTML(None, None).encode("utf-8"))
#as file opened in binary, we can write there encoded bytes sequence, cyrillic one this case






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












