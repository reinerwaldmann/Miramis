#!/usr/bin/python3.4
#!C:\Python33\python.exe

#-*- coding: utf-8

__author__ = 'reiner'
from classes import *
import datetime as dt
import dateutil.parser as dparser

import xml.etree.ElementTree as ET


testfilename='sandbox/03_12_2014_RK_191.xml'

tree=ET.parse(testfilename)
root=tree.getroot()

#root = ET.fromstring(country_data_as_string)



typeOfReport=root.find('typeOfReport').text
model=root.find('model').text
typeOfTest=root.find('typeOfTest').text
channels = [x.text for x in list(root.find('channelnames'))]


operator=root.find('operator').text
testDateTime=root.find('testDateTime').text
testTime=testDateTime.split(' ')[1]


numOfProduct=root.find('numOfAProduct').text
numOfBatch=root.find('numOfABatch').text
hasPassedTest=bool(int(root.find('hasPassedTest').text))
proceduresResultsXML=list(root.find ('proceduresResults'))

def parseResultToProcedureProtocol(rx):
    """
    Парсит xml в процедуру из протокола
    :param rx xml представление
    """
    prc = Procedures()
    prc.number=int(rx.attrib['number'])
    prc.name=rx.find('name').text


    #более эффективно с точки зрения прохода по циклу (один против двух)
    # for mode_common in rx.find('modes_common'):
    #     key=mode_common.find('modename')
    #     value=mode_common.find('value')


    #или более питонически, но чистый ад по производительности (два прохода по циклу)
    #ну и чуть упоротости ибо функция в функции, возможно, поимеет смысл снести и вынести в отдельную
    def modedict(xmlel):
        modes_common_nodes=xmlel
        keys=[mode_common.find('modename').text for mode_common  in modes_common_nodes]
        vals=[mode_common.find('modevalue').text for mode_common  in modes_common_nodes]
        return dict(zip(keys,vals))

    prc.mode_common=modedict(rx.find('modes_common'))





    # mode_common=dict() # словарь общих режимов имя-значение
    # mode_channel=dict(dict()) # словарь словарей режимов по каналам (имя канала - имя параметра - значение)
    # normal_values=dict(dict()) # словарь словарей значений нормативов название канала-название параметра-строка больше-меньше (значение параметра)
    # listOfPossibleResults=list()  # список полей результатов, каковые должны быть отражены в протоколе




    return prc



def parseResultToProcedureResult(resxml):
    """
    Парсит xml в результат
    :param resxml xml представление
    """
    pass






print(typeOfReport)
print(model, typeOfTest, channels)
print(operator, testDateTime, testTime, hasPassedTest)

print(numOfProduct,numOfBatch)


print('\nprtpp:', parseResultToProcedureProtocol(proceduresResultsXML[0]))
