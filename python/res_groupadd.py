#!/usr/bin/python3.4
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

# watchfolder="C:\Program Files (x86)\Apache Software Foundation\Apache2.2\htdocs\groupadd_reswatchfolder\\"
# putfolder="C:\Program Files (x86)\Apache Software Foundation\Apache2.2\htdocs\groupadd_resputfolder\\"
# logfile="C:\Program Files (x86)\Apache Software Foundation\Apache2.2\htdocs\groupadd_log.txt"

watchfolder="/home/r_uploader/groupadd_reswatchfolder/"
putfolder="/home/r_uploader/groupadd_resputfolder/"
logfile="/var/log/miramis/report_groupadd.txt"




def log (strm):
    """
    Записать лог в файл
    @strm - сообщение
    """
    global logfile
    with open(logfile, "a+t") as f:
        f.write(strm)



def process():
    global watchfolder, putfolder



    #получить список файлов
    files = os.listdir(watchfolder)
    textfiles = list(filter(lambda x: x.endswith('.TXT') or x.endswith('.txt'), files))
    report="[INFO] Process {0} {1}\n".format(watchfolder, putfolder)

    #TODO сюда добавить добавление xml

    for name in textfiles:

        #print (prs.parseToResult (watchfolder+name))
        #отсылка к бакенду - добавление результата в базу данных
        report+=name + "\n"
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

        rs = prs.parseToResultCP1251 (watchfolder+name)
        if rs==None:
            report+="[ERROR] "+st+" Не удалось распарсить результат имя файла="+name+"\n"

       # print (rs)


        #сперва попробуем перенести файл
        mvs=1
        try:
            shutil.move(watchfolder+name, putfolder)
        except BaseException:
            log ("[ERROR]"+st+"Проблема при перемещении файла, возможно дублирование отчёта")
            print ("[ERROR]"+st+"Проблема при перемещении файла, возможно дублирование отчёта")
            mvs=0

        if mvs:
            wr=bmr.writeResultToDatabase(rs);
            if wr:
                report+="[ERROR] "+st+" При записи в БД произошла ошибка код="+str(wr)+"\n"

            report+="\t"+st+"Запись в БД произошла успешно "+name+"\n"


    log (report)
    print (report)




#testarea

process()














