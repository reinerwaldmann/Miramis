from structure.classes import AProtocol

__author__ = 'vasilev_is'

from structure.parsers import *

import pickle

from mydbconnect import dbdesc


def upload_to_protocol(filedescriptor):
    """
    Загружает протокол из файла в базу данных. Пока через Pickle
    """
    db=dbdesc()
    cursor=db.cursor()
    protocol=parseToAProtocol(filedescriptor)
    pickled=pickle.dumps(protocol)

    #вкатываем протокол в базу данных через pickle
    sql = """INSERT INTO protocols(ProductName, TestName, Pickle)
        VALUES (%(model)s, %(testname)s ,  %(pickl)s)
        """.format(protocol.typeOfTest)
    #print (sql)

        # исполняем SQL-запрос
    cursor.execute(sql,  {'model':protocol.model, 'testname':protocol.typeOfTest, 'pickl': pickled})

        # применяем изменения к базе данных
    db.commit()

# CREATE TABLE `protocols` (
#   `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `ProductName` text,
#   `TestName` text,
#   `Pickle` blob,
#   `XML` text,
#   `Text` text,
#   PRIMARY KEY (`ID`)
# model=str()
 #    typeOfTest=str()


def upload_to_result(filedescriptor):
    """
    Грузит в базу данных
    """
    pass



#debugging procedures
def test ():
    """
    for debugging
    """
    filename="sandbox/protocolCP1251.txt"

# import platform
# #print (platform.system())
#
# if (platform.system().__contains__("Linux")):
#     filename="utf8.txt" #и вот тут должно быть перекодирование, тащемта
# else:

    try:
        file=open(filename, "r")
    except:
        print("Error while opening file")
        return
    upload_to_protocol(file)

test()



