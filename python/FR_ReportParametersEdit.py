#!/usr/bin/python3.4
#!C:\Python33\python.exe

#-*- coding: utf-8

from classes import *
import htmlgeneralfunctions as htmg
import backend_manageProtocols as bck
import cgitb, cgi, io, sys, os


cgitb.enable()


def outFilledFormCore (protocol, name, id):
    """
    Пустую форму выводит, если параметров отчётной формы с таким именем найти не удалось
    """
    res=str()
    reportFormParameters = None
    nm=""
    if name in protocol.dictOfReportFormParameters: #что позволяет применять стрёмные опции в комбобоксе вызывной формы
        reportFormParameters=protocol.dictOfReportFormParameters[name]
        nm=name
        res+="<br/> <input type='button' onclick=\"destroy('Вы уверенно хотите удалить данный набор параметров?', 'FR_ReportParametersEdit.py?id={0}&name={1}&del=1' ) \"   value='Удаление'  >  <br/> ".format(id, name)

    res+="<input type='text' name='name' value='{0}'> <br/>".format (nm)

    res+= """
    <table border=1 class='itemstable'> <tr> <td> Процедура </td> <td> Общие параметры </td> <td> Поканальные параметры </td> </tr>
    """
    for key, procedure in protocol.procedures.items():
            res+=str("""<tr> \n  <td> {0} </td> \n  <td> {1} </td> \n  <td> {2} </td>\n  </tr> \n """).\
                format(key,
                       outLst (procedure.listOfPossibleResultsCommon, reportFormParameters.dictOfProceduresParameters[key].listOfHiddenCommonParameters if reportFormParameters and key in reportFormParameters.dictOfProceduresParameters else None, str(key) + "_com"),
                       outLst (procedure.listOfPossibleResults, reportFormParameters.dictOfProceduresParameters[key].listOfHiddenPerchannelParameters if reportFormParameters and key in reportFormParameters.dictOfProceduresParameters else None, str(key)+ "_chn"),

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
               outFilledFormCore(proc[0], name, procid) + \
               "<input type='submit' value='Сохранить'> "+"</form>"



def delCameData(form): #удаление
    id=int(form.getfirst("id", ""))
    name = form.getfirst("name", "")
    prot=bck.getProtocolFromDatabase(id)[0] # Возвращает объект испытания
    try:
        del prot.dictOfReportFormParameters[name]
    except KeyError:
        pass

    return bck.writeProtocolToDatabase(prot, id)




def saveCameData(form):
    id=int(form.getfirst("id", ""))
    name = form.getfirst("name", "")
    prot=bck.getProtocolFromDatabase(id)[0] # Возвращает объект испытания

    rfp = ReportFormParameters()
    rfp.dictOfProceduresParameters=dict()

    if  prot==None:
        return 1


    for key in form.keys():


        if "chn" in key or "com" in key:
            ls=key.split('_')
            number = int(ls[0])
            var = key[key.rfind('_')+1::]

            if number in rfp.dictOfProceduresParameters:
            #если есть такой ключ процедуры, что может получиться в том случае, если для такой процедуры параметры мы уже находили
            #тогда просто добавляем в нужный список название пеерменной
                if "chn" in key:
                    rfp.dictOfProceduresParameters[number].listOfHiddenPerchannelParameters.append(var)
                if "com" in key:
                    rfp.dictOfProceduresParameters[number].listOfHiddenCommonParameters.append(var)
            else: #иначе придётся сперва создать объект параметров процедуры
                procparam=ProcedureReportFormParameters()

                procparam.listOfHiddenPerchannelParameters=list()
                procparam.listOfHiddenCommonParameters=list()


                if "chn" in key:
                    procparam.listOfHiddenPerchannelParameters.append(var)
                if "com" in key:
                    procparam.listOfHiddenCommonParameters.append(var)
                rfp.dictOfProceduresParameters[number]=procparam
                #добавляем параметры процедуры



    if not prot.dictOfReportFormParameters: #на кой этот сиране костыль, но Питоний не понимает, что поле является словарём, пока ему не скажешь об этом
        prot.dictOfReportFormParameters=dict()

    prot.dictOfReportFormParameters[name]=rfp
    #либо создаёт, либо перезаписывает параметры процедуры под таким названием


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
        #debug
        else:
            htmg.out("<br/>Сохранено успешно<br/>")

    if "del" in form: #запрос на удаление
        if delCameData(form): #удаление
            #если ошибка
            htmg.out(htmg.throwError("FR_ReportParametersEdit.py", "Ошибка при удалении"))
            htmg.out(htmg.generateHTMLFooter())
            exit(0)
        else:
            htmg.out ("<script language = 'javascript'> document.location.href = \"FRprotocolViewEdit.py?id={0}\"; </script> ".format(id))
            htmg.out(htmg.generateHTMLFooter())
            exit(0)




    if "name" in form:
        name=form.getfirst("name", "")
        htmg.out(outFilledForm (id, name))

    else:
        htmg.out(outFilledForm (id, None))

htmg.out(htmg.generateHTMLFooter())
