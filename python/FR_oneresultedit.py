#!C:\Python33\python.exe

#-*- coding: utf-8

__author__ = 'vasilev_is'
from  classes import *
import htmlgeneralfunctions as htmg
import backend_manageProtocols as bck
import backend_manageResults as bmr
import cgitb, cgi, io, sys, os
cgitb.enable()




#HERE JUST FOR INSPIRATION
def outNormalForm (id):
    """
    Выводит пустую форму.
    @id - айди протокола, в который испытание надо будет добавить
    """
    #получить протокол из базы
    #оттуда взять список каналов
    #на основе этого списка пстроить форму
    protocol = bck.getProtocolFromDatabase(id)[0];
    if protocol==None:
        return htmg.throwError("FRtestedit", "Нет такого протокола, испытание которого намереваемся править")

    listchannels = protocol.channelname
    out=" <script> \n  add_forms_to_table("+listchannels.__str__()+" ); </script>"
    return out



#HERE JUST FOR INSPIRATION
def outFilledFormResult(resultsOfProcedure):
    """
    Выводит заполненную форму

    @resultsOfProcedure - результат процедуры, объект
    """

    out=outNormalForm(id)
    proc=bck.getTestFromProtocol (id, procid) # Возвращает объект испытания


    if  proc==None:
        out+=htmg.throwError("FRtestedit", "Нет такого испытания в протоколе, которое мы намереваемся править")
        return out

    out+="\n<script>\n";

    #  number=int() # номер порядковый
    # name=""  # имя процедуры
    # mode_common=dict() # словарь общих режимов имя-значение
    # mode_channel=dict(dict()) # словарь словарей режимов по каналам (имя канала - имя параметра - значение)
    # normal_values=dict(dict()) # словарь словарей значений нормативов название канала-название параметра-строка больше-меньше (значение параметра)
    # listOfPossibleResults=list()  # список полей результатов, каковые должны быть отражены в протоколе
    out+="var name=\""+proc.name+"\";\n"
    out+="var pars="+proc.listOfPossibleResults.__str__()+";\n"

    out+="var mode_common="+proc.mode_common.__str__()+";\n"
    out+="var mode_channel="+proc.mode_channel.__str__()+";\n"
    out+="var normal_values="+proc.normal_values.__str__()+";\n"
    out+="""
    fillListform(pars, 'pars');
    fillDictForm (mode_common, 'mode_common');
    fillDict2DictForm (mode_channel, 'mode_channel');
    fillDict2DictForm (normal_values, 'normal_values');
    setname(name, 'name');
    """

    out+="</script>\n";

    return out


def outGeneral(id):
    pass


def writeTestFromInputParameters(form):
    pass



#у этой страницы могут быть три параметра - id, то есть айди протокола, есть всегда и может быть idtest - айди испытания
#ещё параметр saveid - тогда значит надо сохранить (т. е. добавить или перезаписать) введённое испытание

form = cgi.FieldStorage()

if "saveid" in form:
    htmg.out ("Content-Type: text/html;charset=utf-8\n\n")
    htmg.out(writeTestFromInputParameters(form))
    exit(0)

#вызвать сохраение данных и выйти из скрипта!

if "id" not in form:
    htmg.out(htmg.generateHTMLMetaHeader())
    htmg.out(htmg.throwError("FR_oneresultedit.py", "Не получен ID результата"))
    htmg.out(htmg.generateHTMLFooter())
    exit(0) #а  можно ли вообще так выходить из cgi?

id=int(form.getfirst("id", ""))
htmg.out(outGeneral(id))

if "testedit" in form:
    testedit=int(form.getfirst("testedit", ""))
    htmg.out(outFilledForm (id, testedit))
else:
    htmg.out(outNormalForm (id))

htmg.out(htmg.generateHTMLFooter())











