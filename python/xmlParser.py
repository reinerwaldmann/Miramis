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




def todict(xmlel, names):
    modes_common_nodes=xmlel
    keys=[mode_common.find(names[0]).text for mode_common  in modes_common_nodes]
    vals=[mode_common.find(names[1]).text for mode_common  in modes_common_nodes]
    return dict(zip(keys,vals))

def toDicttodict(xmlel,names):
    keys = [topel.attrib['channame'] for topel in xmlel]
    vals = [todict(topel,names[1::]) for topel in xmlel ]
    return dict(zip(keys,vals))



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


    prc.mode_common=todict(rx.find('modes_common'), ('modename', 'modevalue'))
    prc.mode_channel=toDicttodict(rx.find('channels_modes'),('channel_modes', 'modename', 'modevalue'))






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
