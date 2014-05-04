
import datetime
from datetime import datetime
from numpy.lib.shape_base import tile


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
        res=self.model
        res+="\n"+self.typeOfTest
        res+="\n"+self.channelname
        res+="\n"+self.procedures
        return res

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
    proceduresResults=dict() #номер испыания - resultsOfProcedure
   # def __str__(self):
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
    number=int()
    hasPassedProcedure=bool()
    values=dict()  #словарь словарей название канала - название параметра - значение
    def __str__(self):
        return self.__dict__.__str__()
        #print (self.number.__str__())
        #print (self.hasPassedProcedure.__str__())
        #print(self.values.__str__())



#Эта функция - ещё тестовая. Она будет впихивать данные из протокола в класс AResult
def parseToResult (filename):
    try:
        file=open(filename, "r")
    except:
        print("Error while opening file")

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








    print(res)


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
parseToResult ("sandbox/utf8.txt")












