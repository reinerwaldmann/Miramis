#!/usr/bin/python3.4
class BaseStrReturn:
    """
    Класс, описывающий метод, который возвращает все значения полей класса в строковом виде
    """
    def __str__(self):
        res="["+type(self).__name__+"]\n"
        for line, value in self.__dict__.items():
            res+=line+":\t"+value.__str__()+"\n"
        return res

class AProtocol(BaseStrReturn):
    """
    Класс, представляющий тип протокола (т. е. тип изделие - испытания)
    """
    model=str()
    typeOfTest=str()
    channelname=list()



    procedures=dict()  # словарь номер процедуры - процедура

    dictOfReportFormParameters = dict() #Словарь классов параметров отчётных форм 'название' - класс


    def __str__(self):
        res=BaseStrReturn.__str__(self)
        for key, val in self.procedures.items():
            res+=str(key)+" : "+val.__str__().replace("\n", "\n\t")   #выводим с отступом
        return res


class ReportFormParameters (BaseStrReturn):
    """
    Содержит в себе информацию о параметрах выходных отчётных форм
    """
    dictOfProceduresParameters  = dict () #словарь айди процедуры - класс параметров процедуры

class ProcedureParameters (BaseStrReturn):
    """
    Содержит в себе информцию о спрятываемых параметрах применительно к одной процедурке
    """
    listOfHiddenCommonParameters = list()
    listOfHiddenPerchannelParameters = list()






class Procedures(BaseStrReturn):
    """
    Класс, представляющий процедуру из типа протокола
    """
    number=int() # номер порядковый
    name=""  # имя процедуры
    mode_common=dict() # словарь общих режимов имя-значение
    mode_channel=dict(dict()) # словарь словарей режимов по каналам (имя канала - имя параметра - значение)

    normal_values=dict(dict()) # словарь словарей значений нормативов название канала-название параметра-строка больше-меньше (значение параметра) поканальный
    normal_values_common=dict() # словарь словарей значений нормативов название канала-название параметра-строка больше-меньше (значение параметра) общий


    listOfPossibleResults=list()  # список полей результатов, каковые должны быть отражены в протоколе поканальные
    listOfPossibleResultsCommon=list()  # список полей результатов, каковые должны быть отражены в протоколе общие






    def toHTML(self, out3=1):      #переводит подержимое в левую половину строки в протоколе (первые три ячейки)
        try:
            """
            Производит html-представление в виде нескольких ячеек
            """
            nopr=self.listOfPossibleResults.__len__() #numOfPossibleResults
            #Выводим название процедуры в первую колонку
            #res="<td rowspan={0}>{1}</td>\n".format(nopr,  str(self.number)+" "+self.name)
            res="<td>{0}</td>\n".format(str(self.number)+" "+self.name.strip())
            #Выводим вторую колонку - требования к режимам
            modereprcm=""
            for k, v in  self.mode_common.items():
                modereprcm+="{0}={1}</br>\n".format(k.strip(), v.strip())
            modechannelrepr="Режим по каналам</br>"
            for k in self.mode_channel.keys():
                modechannelrepr+="{0}: </br>".format(k.strip())
                for k, v in  self.mode_channel[k].items():
                    modechannelrepr+="{0}={1}</br>\n".format(k.strip(), v.strip())
            #res+="<td rowpan={0}>{1}</td>\n".format(nopr, modereprcm + "</br>"+ modechannelrepr)
            res+="<td >{0}</td>\n".format(modereprcm.strip() + "</br>"+ modechannelrepr.strip())


            #Выводим третью колонку - нормы по ТУ
            norms=""

            if self.normal_values_common:
                norms+="Общие: <br/>"

            for k, v in self.normal_values_common.items():
                norms+="{0}:</br>{1}</br>\n".format(k.strip(), v.strip())

            for k in self.normal_values.keys():
                norms+="{0}: </br>".format(k)
                for k, v in  self.normal_values[k].items():
                    norms+="{0}:</br>{1}</br>\n".format(k.strip(), v.strip())
            #res+="<td rowspan={0}>{1}</td>\n".format(nopr, norms)



            res+="<td >{0}</td>\n".format(norms)

            #выводим четвёртую полонку - названия величин


            valnames=""

            if self.listOfPossibleResultsCommon:
                valnames+="Общие параметры <br/>"
            for km in self.listOfPossibleResultsCommon:
                valnames+=km+"</br>"

            if self.listOfPossibleResults:
                valnames+="Поканальные параметры <br/>"
            for km in self.listOfPossibleResults:
                valnames+=km.strip()+"</br>"
            if out3:
                res+="<td>{0}</td>".format(valnames)


            return res
        except BaseException:
            return ""



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


#Представляет результат процедуры
class resultsOfProcedure(BaseStrReturn):
    #парсит в resultsOfProcedure, каковой и возвращает.
    number=int()
    hasPassedProcedure=bool()
    values1=dict()  #словарь словарей название канала - название параметра - значение

    values_common=dict()  #словарь название параметра-значение для общих величин

    def __str__(self):
        res = BaseStrReturn.__str__(self)   #по непонятной причине, BaseStrReturn отказывается выводить словарь словарей
        return res

    def toHTML(self):
        """
        Возвращает HTML представление результатов, сиречь содержание ячейки.
        Теги ячейки не включаются в оную строку
        """
        res="{0} </br>".format("[Пройдена]" if self.hasPassedProcedure else "[Не пройдена]") #вариант тернарного оператора в Python

        valrepr=""
        for k in self.values1.keys():
            valrepr+="{0}: </br>".format(k)
            for k, v in  self.values1[k].items():
                valrepr+="{0}={1}</br>\n".format(k, v)

        valrepr+="{0}: </br>".format("Общие")
        for k in self.values_common.keys():
            valrepr+="{0}={1}</br>\n".format(k, self.values_common[k])

        res+=valrepr

        return res


