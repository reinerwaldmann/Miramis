__author__ = 'vasilev_is'

from classes import *
from mydbconnect import dbdesc
import pickle


#[BACKEND]

"""
В этом файле описываются фукнкции, работающие с протоколами, в частности, с оными в базе данных

addTestToProtocol (idprotocol, procd, desiredid=None) #Добавить испытание в протокол
    @idprotocol - айди протокола в базе
    @procd: Procedures, которую добавляем
delTestFromProtocol(idprotocol, idtest): Удаляет испытание из протокола, idprotocol - айди протокола, idtest - айди испытания
    @idprotocol - айди протокола
    @idtest - айди испытания
writeProtocolToDatabase(protocol, idprotocol=None): Записать протокол в базу данных
    @protocol - объект протокола
    @idprotocol - если задано, то пишет на этот айди. Если таковой айди имеется в базе данных, то проиcходит обязательная перезапись
    getProtocolFromDatabase(id) Получить протокол из базы данных
    @id: айди в базе данных
    getTestFromProtocol (idprotocol, idtest) Возвращает объект испытания
    @idprotocol - айди протокола
    @idtest - айди испытания

    getProtocolFromDatabaseParams (ProductName, TestName):
    Получить протокол из базы данных
    @ProductName - имя продукта
    @TestName - имя теста


"""


def getTestFromProtocol (idprotocol, idtest):
    """
    @idprotocol - айди протокола
    @idtest - айди испытания

    Возвращает объект испытания
    """

    protocol = getProtocolFromDatabase(idprotocol)[0]
    if protocol==None:
        return 1
    try:
        return protocol.procedures[idtest]
    except BaseException:
        return None




def addTestToProtocol (idprotocol, procd, desiredid=None):
    """
    @idprotocol - айди протокола в базе
    @procd: Procedures, которую добавляем
    Добавляет испытание в протокол. desiredid - айди, под которым её хотим добавить. Если None, то вычисляется автоматически.
    Если нет, то заменяет таковой ключ в словаре данным. Здесь может быть перезапись, либо дописывание - ситуация в данной версии
    не регламентирована
    """
    protocol = getProtocolFromDatabase(idprotocol)[0]
    if (protocol==None):
        return 1

    #вычисление максимального айди
    id=desiredid

    if (desiredid==None):
        id=0
        for i in protocol.procedures.keys():
            id=max(id, i)
        id+=1

    procd.number=id
    protocol.procedures[id]=procd

    return writeProtocolToDatabase(protocol, idprotocol)


def delTestFromProtocol(idprotocol, idtest):
    """
    @idprotocol - айди протокола
    @idtest - айди испытания
    Удаляет испытание из протокола
    Выдернуть из базы - изменить - вкатать в базу
    """
    # получить протокол
    # снести в протоколе нужное испытание
    # вкатать протокол
    # если на этапе ошибка - прерваться, вернуть 1

    protocol = getProtocolFromDatabase(idprotocol)[0]
    if protocol==None:
        return 1
    try:
        del (protocol.procedures[idtest])
    except KeyError:
        return 2
    if writeProtocolToDatabase(protocol, idprotocol):
        return 3

    return 0


def writeProtocolToDatabase(protocol, idprotocol=None):
    """
    Пишет протокол в базу данных
    @protocol - объект протокола
    @idprotocol - если задано, то пишет на этот айди. Если таковой айди имеется в базе данных, то проиcходит перезапись.
    """
    db=dbdesc()
    cursor=db.cursor()
    pickled=pickle.dumps(protocol)

    if (idprotocol==None):
        #вкатываем протокол в базу данных через pickle
        sql = """INSERT INTO protocols(ProductName, TestName, Pickle)
            VALUES (%(model)s, %(testname)s ,  %(pickl)s)
            """
        #print (sql)
    # исполняем SQL-запрос
        try:
            cursor.execute(sql,  {'model':protocol.model, 'testname':protocol.typeOfTest, 'pickl': pickled})
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
            db.close()
            return 1

    else:   #если  айди задан
        #то сперва надо удалить такой айди в базе, если он, правда, есть. Если такого нет, то надо выкинуть ошибку наверное (?)

        sql = "DELETE FROM protocols WHERE ID='"+str(idprotocol)+"'"
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            db.close()
            return 1  #ключевой момент - если не найдено такого айди, то вернуть один и ничего не делать



        #вкатываем протокол в базу данных через pickle
        sql = """INSERT INTO protocols(ID, ProductName, TestName, Pickle)
            VALUES (%(ID)s,  %(model)s, %(testname)s ,  %(pickl)s)
            """
        #print (sql)
    # исполняем SQL-запрос
        try:
            cursor.execute(sql,  {'ID':idprotocol,'model':protocol.model, 'testname':protocol.typeOfTest, 'pickl': pickled})
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
            db.close()
            return 1


    # disconnect from server
    db.close()
    return 0


def getProtocolFromDatabase (id):
    """
    Получить протокол из базы данных
    @id: айди в базе данных
    """
    db=dbdesc()
    cursor = db.cursor()
    sql= "Select * from protocols where id = {0} ;".format(id)
    cursor.execute (sql)  #может вытряжнуть какое-нибудь исключение

    ## Dump the results to a string
    rows = cursor.fetchall()

    if (len(rows)==0):  #если такого нет
        return None, "Error, no such protocol in database"

    ## Get the results
    result=rows[0]
    return pickle.loads(rows[0][3]), rows[0][1], rows[0][2]



def getProtocolFromDatabaseParams (ProductName, TestName):
    """
    Получить протокол из базы данных
    @ProductName - имя продукта
    @TestName - имя теста
    """
    db=dbdesc()
    cursor = db.cursor()
    sql= "Select * from protocols where ProductName = '{0}' and TestName = '{1}';".format(ProductName, TestName)


    cursor.execute (sql)  #может вытряжнуть какое-нибудь исключение

    ## Dump the results to a string
    rows = cursor.fetchall()

    if (len(rows)==0):  #если такого нет
        return None, "Error, no such protocol in database"

    ## Get the results
    result=rows[0]
    return pickle.loads(rows[0][3]), rows[0][1], rows[0][2]


