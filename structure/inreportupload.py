from structure.classes import AProtocol

__author__ = 'vasilev_is'

from structure.parsers import *
import mysql.connector
from mysql.connector import errorcode
import pickle

def dbdesc ():
    return mysql.connector.connect(user='root', passwd='123',host='localhost', db='MiramisDB')

def upload_to_protocol (filedescriptor):
    db=dbdesc()
    cursor=db.cursor()
    protocol=parseToAProtocol(filedescriptor)


    #вкатываем протокол в базу данных через pickle
    sql = """INSERT INTO protocols(ProductName, TestName, Pickle)
        VALUES ('{0}', '{1}', '{2}')
        """.format(protocol.model, protocol.typeOfTest, pickle.dumps(protocol))




        # исполняем SQL-запрос
    cursor.execute(sql)
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
    pass





#debugging procedures
def test ():
    """
    for debugging
    """



# import platform
# #print (platform.system())
#
# if (platform.system().__contains__("Linux")):
#     filename="utf8.txt" #и вот тут должно быть перекодирование, тащемта
# else:
    filename="sandbox/protocolCP1251.txt"

    try:
        file=open(filename, "r")
    except:
        print("Error while opening file")
        return
    upload_to_protocol(file)

test()


