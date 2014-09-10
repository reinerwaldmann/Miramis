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

    dictOfReportFormParameters = dict() #Словарь классов параметров отчётных форм 'название' - класс

    procedures=dict()  # словарь номер процедуры - процедура
    def __init__(self):
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
    dictOfProceduresParameters=dict() #словарь айди процедуры - класс параметров процедуры

class ProcedureReportFormParameters (BaseStrReturn):
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






    def toHTML(self, out3=1, prfp=None):      #переводит подержимое в левую половину строки в протоколе (первые три ячейки)
        """
        Производит html-представление в виде нескольких ячеек
        prfp - ProcedureReportFormParameters, параметры спрятываемых величин
        """

        lhp_com=list()
        lhp_chn=list()

        res="<td>{0}</td>\n".format(str(self.number)+" "+self.name.strip())

        try:
            lhp_com=prfp.listOfHiddenCommonParameters
            lhp_chn=prfp.listOfHiddenPerchannelParameters
        except BaseException:
            pass

        try:
            nopr=self.listOfPossibleResults.__len__() #numOfPossibleResults
            #Выводим название процедуры в первую колонку
            #res="<td rowspan={0}>{1}</td>\n".format(nopr,  str(self.number)+" "+self.name)

            #Выводим вторую колонку - требования к режимам
            modereprcm=""


            klist=list(self.mode_common.keys())
            klist.sort()

            for k in klist:
                v=self.mode_common[k]
            #for k, v in  self.mode_common.items():
                modereprcm+="{0}{1}{2}</br>\n".format(k.strip(),"=" if k.strip() and v.strip() else ""   , v.strip())
            modechannelrepr="Режим по каналам</br>"



            klist=sorted(list(self.mode_channel.keys()))

            for k in klist:
                v=self.mode_channel[k]
            #for k in self.mode_channel.keys():
                modechannelrepr+="{0}: </br>".format(k.strip())

                mlist=list(self.mode_channel[k].keys())
                mlist.sort()
                for mm in mlist:
                    v = self.mode_channel[k][mm]

                #for k, v in  self.mode_channel[k].items():
                    modechannelrepr+="{0}{1}{2}</br>\n".format(mm.strip(), "=" if mm.strip() and v.strip() else "", v.strip())

            #res+="<td rowpan={0}>{1}</td>\n".format(nopr, modereprcm + "</br>"+ modechannelrepr)
            res+="<td >{0}</td>\n".format(modereprcm.strip() + "</br>"+ modechannelrepr.strip())


            #Выводим третью колонку - нормы по ТУ
            norms=""

            if self.normal_values_common:
                norms+="Общие: <br/>"


            klist = list(self.normal_values_common)
            klist.sort()

            for k in klist:

                v=self.normal_values_common[k]


            #for k, v in self.normal_values_common.items():
                if not lhp_com or (lhp_com and not k in lhp_com):
                    norms+="{0}:</br>{1}</br>\n".format(k.strip(), v.strip())



            klist = list(self.normal_values.keys())
            klist.sort()


            for k in klist:#по каналам
            #for k in self.normal_values.keys():
                norms+="{0}: </br>".format(k)

                mlist = list(self.normal_values[k].keys())
                mlist.sort()

                for m in mlist: #по величинам
                    v = self.normal_values[k][m]
                #for k, v in  self.normal_values[k].items():
                    if not lhp_chn or (lhp_chn and not m in lhp_chn):
                        norms+="{0}:</br>{1}</br>\n".format(m.strip(), v.strip())
            #res+="<td rowspan={0}>{1}</td>\n".format(nopr, norms)



            res+="<td >{0}</td>\n".format(norms)

            #выводим четвёртую полонку - названия величин


            valnames=""

            if self.listOfPossibleResultsCommon:
                for km in sorted(self.listOfPossibleResultsCommon):
                    if not lhp_com or (lhp_com and not km in lhp_com):
                        valnames+=km+"</br>"
                if valnames:
                    valnames="Общие параметры: <br/>"+valnames


            if self.listOfPossibleResults:
                valnames_1=""
                for km in sorted(self.listOfPossibleResults):
                    if not lhp_chn or (lhp_chn and not km in lhp_chn):
                        valnames_1+=km.strip()+"</br>"
                if valnames_1:
                    valnames_1="Поканальные параметры: <br/>"+valnames_1
                    valnames+=valnames_1




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

    def toHTML(self, prfp=None):
        """
        Возвращает HTML представление результатов, сиречь содержание ячейки.
        Теги ячейки не включаются в оную строку
        prfp - ProcedureReportFormParameters, параметры спрятываемых величин
        """
        res="{0} </br>".format("[Пройдена]" if self.hasPassedProcedure else "[Не пройдена]") #вариант тернарного оператора в Python

        lhp_com=list()
        lhp_chn=list()


        try:
            lhp_com=prfp.listOfHiddenCommonParameters
            lhp_chn=prfp.listOfHiddenPerchannelParameters
        except BaseException:
            pass


        valrepr=""

        klist=list(self.values1.keys())
        klist.sort()

        for kk in klist: #по каналам
            vlp=""
            varlistl=list(self.values1[kk].keys())
            varlistl.sort()

            for k in varlistl:
                v=self.values1[kk][k]
            #for k, v in  self.values1[kk].items():
                if not lhp_chn or (lhp_chn and not k in lhp_chn):
                    vlp+="{0}={1}</br>\n".format(k, v)
            if vlp:
                valrepr+="{0}: </br>".format(kk)+vlp







        valreprcom=""


        klist=list(self.values_common.keys())
        klist.sort()
        for k in klist:
            if not lhp_com or (lhp_com and not k in lhp_com):
                valreprcom+="{0}={1}</br>\n".format(k, self.values_common[k])
        if valreprcom:
            valreprcom="{0}: </br>".format("Общие параметры")+valreprcom
            valrepr+=valreprcom

        res+=valrepr

        return res


def sba(inputStr):
        return inputStr[0] # Ключом является первый символ в каждой строке, сортируем по нему