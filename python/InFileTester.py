__author__ = 'vasilev_is'
#Это специальный файл для тестирования корректности формата входящих файлов


import parsers as prs
import os


def testTextProtocols (filename):
    assert os.path.exists(filename), "I did not find the file at, "+str(filename) #проверяет значения произвольных данных

    with open(filename, 'rt') as file:
        protocol = prs.parseToAProtocolCP1251(file) #распарсили протокол
        result = prs.parseToResult(filename)


    print ('parsed protocol')
    print (protocol)

    print ('parsed result')
    print (result)


testTextProtocols(input('Enter path'))

