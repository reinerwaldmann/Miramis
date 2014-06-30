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
import backend_manageProtocols as bck


watchfolder="C:\Program Files (x86)\Apache Software Foundation\Apache2.2\htdocs\groupadd_reswatchfolder\\"
putfolder="C:\Program Files (x86)\Apache Software Foundation\Apache2.2\htdocs\groupadd_resputfolder\\"
logfile="C:\Program Files (x86)\Apache Software Foundation\Apache2.2\htdocs\groupadd_log.txt\\"




def log (strm):
    """
    Записать лог в файл
    @strm - сообщение
    """
    global logfile
    with open(logfile, "wt") as f:
        f.writeln(strm)



def process():
    global watchfolder, putfolder

    #получить список файлов
    files = os.listdir(watchfolder)
    textfiles = list(filter(lambda x: x.endswith('.txt'), files))


    for name in textfiles:
        #print (prs.parseToResult (watchfolder+name))
        #отсылка к бакенду - добавление результата в базу данных








#testarea

process()














