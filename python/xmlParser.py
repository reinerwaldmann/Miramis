#!/usr/bin/python3.4
#!/usr/bin/python3.4
#!/usr/bin/python3.4
#!C:\Python33\python.exe

#-*- coding: utf-8

__author__ = 'reiner'
from classes import *


import xml.etree.ElementTree as ET
import traceback
testfilename='sandbox/09_12_2014_RK_210.xml'


def todict(xmlel, names):
    modes_common_nodes=xmlel
    keys=[mode_common.find(names[0]).text for mode_common  in modes_common_nodes]
    vals=[mode_common.find(names[1]).text for mode_common  in modes_common_nodes]
    return dict(zip(keys,vals))

def toDicttodict(xmlel,names):
    keys = [topel.attrib['channame'] for topel in xmlel]
    vals = [todict(topel,names[1::]) for topel in xmlel ]
    return dict(zip(keys,vals))



def parsePrc(rx, type=""):
    """
    Парсит xml в процедуру из протокола, если type='prc' иначе в результат процедуры
    :param rx xml представление
    """
    number=int(rx.attrib['number'])
    channelresults=toDicttodict(rx.find('channels_result_values'),('channels_result_values', 'name', 'value'))
    commonresults=todict(rx.find('common_result_values'),('name', 'value'))
    if type=='prc':
        prc = Procedures()
        prc.number=number
        prc.name=rx.find('name').text
        prc.mode_common=todict(rx.find('modes_common'), ('modename', 'modevalue'))
        prc.mode_channel=toDicttodict(rx.find('channels_modes'),('channel_modes', 'modename', 'modevalue'))
        prc.normal_values=toDicttodict(rx.find('channels_normal_values'),('channel_normal_value', 'norm_name', 'norm_value'))
        prc.normal_values_common=todict(rx.find('common_normal_values'),('norm_name', 'norm_value'))
        prc.listOfPossibleResults=list(list(channelresults.items())[0][1].keys())
        prc.listOfPossibleResultsCommon=list(commonresults.keys())
        return prc
    res= resultsOfProcedure()
    #парсинг результатов. его организация намекает нам на целесообразность объединения парсингов в одну функцию, которая вернёт или результат, или протокол, в зависимости от флага входного параметра
    res.hasPassedProcedure=bool(int(rx.find('hasPassedProcedure').text))
    res.number=number
    res.values1=channelresults
    res.values_common=commonresults

    return res

def parceXml(testfilename, type=''):
    """
    Парсит файл в протокол (если type='prc') или в результат, если это не так
    :param testfilename: имя файла
    :param type: 'prc', чтоб парсить в протокол, иначе всё, что угодно, чтоб парсить в результат
    :return: протокол или результат  (объект), лог
    """

    try:
        try:
            tree=ET.parse(testfilename)
            root=tree.getroot()
        except BaseException: #что выйдет, если тип не подходит для функции ET
            root = ET.fromstring(testfilename.read())


        typeOfReport=root.find('typeOfReport').text #должен быть NIST

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
        if type=='prc':
            prc=AProtocol()
            prc.model=model
            prc.typeOfTest=typeOfTest
            prc.channelname=channels
            prc.procedures=dict()
            ffunc=lambda x: parsePrc(x, type="prc")
            proceduresResults=list(map(ffunc, proceduresResultsXML))
            for pp in proceduresResults:
                prc.procedures[pp.number]=pp
            return prc,''

        #else result
        res=AResult()
        res.model=model
        res.typeOfTest=typeOfTest
        res.operator=operator
        res.testDateTime=testDateTime
        res.testTime=testTime
        res.numOfProduct=numOfProduct
        res.numOfBatch=numOfBatch
        res.hasPassedTest=hasPassedTest
        res.proceduresResults=dict()
        proceduresResults=list(map(parsePrc, proceduresResultsXML))
        for pp in proceduresResults:
            res.proceduresResults[pp.number]=pp
        return res,''

    except BaseException as e:
        return None, e.__str__()+"\n"+traceback.format_exc()



def test():
    #root = ET.fromstring(country_data_as_string)
    print(parceXml(testfilename,  'prc')[1])

#test()
