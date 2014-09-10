#!/usr/bin/python3.4
#!/usr/bin/python3.4
#!/usr/bin/python3.4
#!/usr/bin/python3.4
#!/usr/bin/python3.4
__author__ = 'vasilev_is'

from classes import *
from mydbconnect import dbdesc
import pickle


#[BACKEND]

"""
В этом файле описываются фукнкции, работающие с результатами, в частности, с оными в базе данных


    writeResultToDatabase(result, idresult=None): Записать результат в базу данных
    @result - объект результата
    @idresult - если задано, то пишет на этот айди. Если таковой айди имеется в базе данных, то проиcходит обязательная перезапись

    getResultFromDatabase(id) Получить результат из базы данных
    @id: айди в базе данных





"""



def  writeResultToDatabase(result, idresult=None):
    """
    Записать результат в базу данных
    @result - объект результата
    @idresult - если задано, то пишет на этот айди. Если таковой айди имеется в базе данных, то проиcходит обязательная перезапись

    """

    if result==None:
        return 1

    db=dbdesc()
    cursor=db.cursor()
    pickled=pickle.dumps(result)

#
# `ID` int(11) NOT NULL AUTO_INCREMENT,
#   `ProductName` text,
#   `TestName` text,
#   `Operator` text,
#   `Date` datetime DEFAULT NULL,
#   `SerialNumber` text,
#   `BatchNumber` text,
#   `TypeOfTest` text,
#   `Pickle` blob,
#   `XML` text,
#   `Text` text,
#   `resultscol` varchar(45) DEFAULT NULL,


 #
    #          model=str()
    # typeOfTest=str()
    # operator=str()
    # testDateTime=str()
    # testTime=str()
    # numOfProduct=int()
    # numOfBatch=int()
    # hasPassedTest=bool() #1 - прошёл, 0 - не прошйл. Результаты испытаний
    # proceduresResults=dict() #номер испытания - resultsOfProcedure


    if (idresult==None):
        #вкатываем протокол в базу данных через pickle
        sql = """INSERT INTO results(ProductName, TestName, Operator, Date, SerialNumber, BatchNumber, Pickle, hasPassedTest)
            VALUES (%(model)s, %(testname)s ,  %(Operator)s, %(Date)s, %(SerialNumber)s, %(BatchNumber)s, %(pickl)s, %(hasPassedTest)s  )
            """
        #print (sql)
    # исполняем SQL-запрос
        try:

            cursor.execute(sql,  {'model':result.model, 'testname':result.typeOfTest,   'Operator':result.operator,
                                  'Date':result.testDateTime, 'SerialNumber':result.numOfProduct, 'BatchNumber':result.numOfBatch,
                                  'pickl':pickled, 'hasPassedTest':result.hasPassedTest})
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
            db.close()
            return 2


    else:   #если  айди задан
        #то сперва надо удалить такой айди в базе, если он, правда, есть. Если такого нет, то надо выкинуть ошибку наверное (?)

        sql = "DELETE FROM results WHERE ID='"+str(idresult)+"'"
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            db.close()
            return 3  #ключевой момент - если не найдено такого айди, то вернуть один и ничего не делать


        #вкатываем протокол в базу данных через pickle
        sql = """INSERT INTO results(ID, ProductName, TestName, Operator, Date, SerialNumber, BatchNumber, Pickle, hasPassedTest)
            VALUES (%(ID)s,  %(model)s, %(testname)s ,  %(Operator)s, %(Date)s, %(SerialNumber)s, %(BatchNumber)s, %(pickl)s, %(hasPassedTest)s  )
            """


        #print (sql)
    # исполняем SQL-запрос
        #try:
        cursor.execute(sql,  {'ID':str(idresult), 'model':result.model, 'testname':result.typeOfTest,   'Operator':result.operator,
                                  'Date':result.testDateTime, 'SerialNumber':result.numOfProduct, 'BatchNumber':result.numOfBatch,
                                  'pickl':pickled, 'hasPassedTest':result.hasPassedTest})

        db.commit()
        #except:
            # Rollback in case there is any error
        #    db.rollback()
        #    db.close()
        #    return 4

    # disconnect from server
    db.close()
    return 0



def getResultFromDatabase(id):

    """
    Получить результат из базы данных
    @id: айди в базе данных
    """
    db=dbdesc()
    cursor = db.cursor()
    sql= "Select * from results where id = {0} ;".format(id)
    cursor.execute (sql)  #может вытряжнуть какое-нибудь исключение

    ## Dump the results to a string
    rows = cursor.fetchall()

    if (len(rows)==0):  #если такого нет
        return None, "Ошибка, нет такого результата в базе данных"

    ## Get the results
    result=rows[0]
    return pickle.loads(rows[0][8]), rows[0][1], rows[0][2], rows[0][3], rows[0][4], rows[0][5], rows[0][6], rows[0][7], rows[0][11], rows[0][12]



#UNTESTED
def delItemFromResult(idresult, iditem):
    """
    Удаляет испытание из результата
    @idresult - айди результата
    @iditem - айди испытания
    """

    # получить результат
    # снести в результате нужное испытание
    # вкатать результат
    # если на этапе ошибка - прерваться, вернуть 1

    result = getResultFromDatabase(idresult)[0]
    if result==None:
        return 1
    try:
        del (result.proceduresResults[iditem])
    except KeyError:
        return 2
    if writeResultToDatabase(result, idresult):
        return 3

    return 0


#UNTESTED
def getItemFromResult (idresult, iditem):
    """
    Возвращает объект испытания
    @idresult - айди результата
    @iditem - айди испытания
    """
    result = getResultFromDatabase(idresult)[0]
    if result==None:
        return 1
    try:
        return result.proceduresResults[iditem]
    except BaseException:
        return None


#UNTESTED
def addItemToResult (idresult, resulsOfProcedure, desiredid=None):
    """Добавить испытание в результат
    @idresult - айди результата
    @desiredid - айди испытания. Если None, то добавляет. Если установлено, то перезаписывает
    @resulsOfProcedure - результат процедуры

    """
    result = getResultFromDatabase(idresult)[0]
    if result==None:
        return 1

    #вычисление максимального айди
    id=desiredid

    if (desiredid==None):
        id=0
        for i in result.proceduresResults.keys():
            id=max(id, i)
        id+=1

    resulsOfProcedure.number=id
    result.proceduresResults[id]=resulsOfProcedure

    return  writeResultToDatabase(result, id)

