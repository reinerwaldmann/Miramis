#!/usr/bin/python3.4
#!/usr/bin/python3.4
#!/usr/bin/python3.4
#!/usr/bin/python3.4
#!/usr/bin/python3.4
#-*- coding: utf-8

__author__ = 'vasilev_is'
from  classes import *
import htmlgeneralfunctions as htmg
import backend_manageProtocols as bck
import parsers as prs

import cgitb, cgi, io, sys, os
cgitb.enable()

"""
Загрузка протокола в базу данных из файла

"""


def upload_protocol():
    fileitem = form["file"]
    if fileitem.file:
        # It's an uploaded file; count lines
        #strfile = ""

        #for line in fileitem.file:
         #   strfile+=line.decode("cp1251")  #собрали файл в строку
        ap = prs.parseToAProtocolCP1251(fileitem.file) #распарсили протокол

        if ap[0]==None:  #ошибка при парсинге протокола
            htmg.out("<script>  alert(\"Произошла ошибка при загрузке протокола  на этапе парсинга err="+ap[1] + "\"); </script>")
            show_form()
            return

        err=bck.writeProtocolToDatabase(ap[0], idprotocol=None)
        if not err:
            htmg.out("<script> alert(\"Загрузка протокола произошла успешно\");   document.location.replace(\"../MiramisPHP/protocols.php\");   </script>  ")
            return
        htmg.out("<script>  alert(\"Произошла ошибка при загрузке протокола err="+str(err) + "\"); </script>")
        show_form()


        #line = fileitem.file.readline()




def show_form():
    outs= """
    <form action='FRprotocolAdd.py?upl=1' method='post' enctype='multipart/form-data'>
    <label for="file">Имя файла:</label>
    <input type='file'" name='file' id='file'><br>
    <input type='submit' name='submit' value='Загрузить'>
</form>
    """
    htmg.out(outs)

#debugging
#ap = prs.parseToAProtocolCP1251(open("sandbox/protocolCP1251.txt", "rb")) #распарсили протокол



#Если видим какие-нибудь данные, то запускаем добавление протокола
#если нет - то запускаем отображение формы


htmg.out (htmg.generateHTMLMetaHeader("Добавление протокола"))
form = cgi.FieldStorage()

if "upl" in form:
    upload_protocol()
else:
    show_form()




htmg.out(htmg.generateHTMLFooter())





