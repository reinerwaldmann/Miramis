#!C:\Python33\python.exe
#-*- coding: utf-8

__author__ = 'vasilev_is'
from  classes import *
import htmlgeneralfunctions as htmg
import backend_manageProtocols as bck
import parsers as prs

import cgitb, cgi, io, sys, os
cgitb.enable()

"""
Данный скрипт делает групповые отчёты и выводит их в html формате
(пока так, потом, возможно, в зависимости от настроек, и в pdf)

"""

#TODO: Вывод одной отчётной формы (на группу результатов, но на одну печатную страницу)
#TODO: Вывод группы  отчётных форм







htmg.out (htmg.generateHTMLMetaHeader("Вывод отчётной формы"))
form = cgi.FieldStorage()


residlist=list()
#making results list:
for key in form:
    #htmg.out(key+"  "+ form.getfirst(key, "")   +"</br>")
    if "checkbox" in key:
        residlist.append(int(key.split("_")[1]))

htmg.out(residlist.__str__())

htmg.out(htmg.generateHTMLFooter())


