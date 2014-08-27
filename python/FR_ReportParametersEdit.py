#!/usr/bin/python3.4
#!C:\Python33\python.exe

#-*- coding: utf-8

from  classes import *
import htmlgeneralfunctions as htmg
import backend_manageProtocols as bck
import cgitb, cgi, io, sys, os


cgitb.enable()


def outFilledFormCore (protocol, name):
    """
    Пустую форму выводит, если параметров отчётной формы с таким именем найти не удалось
    """
    res=str()
    reportFormParameters = None
    if not name==None and protocol.dictOfReportFormParameters.contains (name):
        reportFormParameters=protocol.dictOfReportFormParameters[name]
    res= """
    <table border=1 class='itemstable'> <tr> <td> Процедура </td> <td> Общие параметры </td> <td> Поканальные параметры </td> </tr>
    """
    for key, procedure in protocol.procedures.items():
        res+=str("""<tr> \n  <td> {0} </td> \n  <td> {1} </td> \n  <td> {2} </td>\n  </tr> \n """).\
            format(key,
                   outLst (procedure.listOfPossibleResultsCommon, reportFormParameters[key].listOfHiddenCommonParameters if reportFormParameters else None, str(key) + "_com"),
                   outLst (procedure.listOfPossibleResults, reportFormParameters[key].listOfHiddenParameters if reportFormParameters else None, str(key)+ "_chn"),

                   )

    return res + """</table>"""

def outLst (lst, hidlst, prefix):
    res=str()

    res+="<table>"
    for i in lst:

        if hidlst==None or not i in hidlst:
            chstr = ""
        else:
            chstr = "checked"


        res+="<tr> <td>"+i+"</td>"+ "<td> <input type='checkbox' name='{0}' {1}> </td> </tr>".format (str(prefix)+"_"+str(i), chstr)+""

    res+="</table>"
    return res









def outFilledForm (procid, name):
    """
    Запускает ядерную функцию, предварительно вынув протокол из базы
    """
    out = str()
    proc=bck.getProtocolFromDatabase(procid) # Возвращает объект испытания

    if  proc[0]==None:
        out+=htmg.throwError("FR_ReportParametersEdit", proc[1])
        return out
    else:
        return "<form method = 'POST' action = 'FR_ReportParametersEdit.py?id={0}&save=1 ' >".format (str(procid))+\
               "<input type='text' name='name' value={0}> <br/>".format (" " if name==None else name) +  \
               outFilledFormCore(proc[0], name) + \
               "<input type='submit' value='Сохранить'> "+"</form>"



def saveCameData(form):
    id=int(form.getfirst("id", ""))
    name = form.getfirst("name", "")

    prot=bck.getProtocolFromDatabase(id) # Возвращает объект испытания

    rfp = ReportFormParameters()



    if  prot[0]==None:
        return 1

    pr = prot[0]



    for key, val in form.items():
        if key.contains("chn") or key.contains("com"):
            ls=key.split('_')
            number = int(ls[0])
            var = key[key.rfind('_')::]

            if number in rfp.dictOfProceduresParameters: #если есть такой ключ процедуры

                if key.contains("chn"):
                    rfp.dictOfProceduresParameters[number].listOfHiddenPerchannelParameters.append(var)
                if key.contains("com"):
                    rfp.dictOfProceduresParameters[number].listOfHiddenCommonParameters.append(var)
            else:
                procparam=ProcedureReportFormParameters()

                if key.contains("chn"):
                    procparam.listOfHiddenPerchannelParameters.append(var)
                if key.contains("com"):
                    procparam.listOfHiddenCommonParameters.append(var)


                rfp.dictOfProceduresParameters[number]=procparam

    prot.dictOfReportFormParameters[name]=rfp
    return bck.writeProtocolToDatabase(prot, id)





form = cgi.FieldStorage()
htmg.out(htmg.generateHTMLMetaHeader())


if "id" not in form:
    htmg.out(htmg.throwError("FR_ReportParametersEdit.py", "Не получен ID протокола"))

else:

    id=int(form.getfirst("id", ""))

    if "save" in form: #запрос на сохранение
        if saveCameData(form): #сохранение
            #если ошибка
            htmg.out(htmg.throwError("FR_ReportParametersEdit.py", "Ошибка при сохранении"))
            htmg.out(htmg.generateHTMLFooter())
            exit(0)


    if "name" in form:
        name=form.getfirst("name", "")
        if not htmg.out(outFilledForm (id, name)):
            htmg.out(outFilledForm (id, None))
    else:
        htmg.out(outFilledForm (id, None))

htmg.out(htmg.generateHTMLFooter())
