__author__ = 'vasilev_is'
"""
Этот файл должен запускаться кроном раз в 5 минут. Он осматривает папку, заданную переменной watchfolder,
и делает следующее:
1. Добавляет (или пытается добавить) файлы оттуда в базу данных результатов
2. Переносит их в папку putfolder
3. Обо всех действиях пишет в файл logfile



"""

import os
import parsers as prs
import backend_manageResults as bmr
import shutil
import datetime
import time

watchfolder="C:\Program Files (x86)\Apache Software Foundation\Apache2.2\htdocs\groupadd_reswatchfolder\\"
putfolder="C:\Program Files (x86)\Apache Software Foundation\Apache2.2\htdocs\groupadd_resputfolder\\"
logfile="C:\Program Files (x86)\Apache Software Foundation\Apache2.2\htdocs\groupadd_log.txt"




def log (strm):
    """
    Записать лог в файл
    @strm - сообщение
    """
    global logfile
    with open(logfile, "wt") as f:
        f.write(strm)



def process():
    global watchfolder, putfolder

    #получить список файлов
    files = os.listdir(watchfolder)
    textfiles = list(filter(lambda x: x.endswith('.txt'), files))
    report=""



    for name in textfiles:
        #print (prs.parseToResult (watchfolder+name))
        #отсылка к бакенду - добавление результата в базу данных

        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

        rs = prs.parseToResult (watchfolder+name)
        if rs==None:
            report+="[ERROR] "+st+" Не удалось распарсить результат имя файла="+name+"\n"

        print (rs)
        wr=bmr.writeResultToDatabase(rs);
        if wr:
            report+="[ERROR] "+st+" При записи в БД произошла ошибка код="+str(wr)+"\n"
        else: #если всё хорошо, записали в базу данных
            shutil.move(watchfolder+name, putfolder)

            report+="\t"+st+"Запись в БД произошла успешно "+name+"\n"

        #копирование сделать в другую папку
    log (report)




#testarea

process()














