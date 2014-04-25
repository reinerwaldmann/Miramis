#!C:\Python34\python.exe
#-*- coding: utf-8

#https://docs.python.org/2/library/cgi.html

#Этот файл для работы с полями  ввода

#для вывода отладочных данных
import cgitb, cgi, io, sys, os
cgitb.enable()

#sys.stdout._encoding = 'utf-8'

def out(msg):
    sys.stdout.buffer.write(msg.encode('utf8'))
    sys.stdout.flush()

out("Content-Type: text/html;charset=utf-8\n\n")
out("<html><head>\n\n")
out("</head><body>\n\n")
out("<h1> ФОРМЫ </h1>")

#https://docs.python.org/3.3/library/cgi.html

form = cgi.FieldStorage()
#if "name" not in form or "addr" not in form:
 #   print "<H1>Error</H1>"
 #   
 #   return
try:

    
    #генераторное выражение
#    print ([(key, form[key].value) for key  in form])


     #выражение с циклом   
    #  for key in form:
  #   print (key, ":-", form[key].value, "</br>")

#ни первое, ни второе не пользовать при использовании POST передачи файлов.

    print ("name\t",form["name"].value)

    fileitem = form["datafile"]
    if fileitem.file:
        # It's an uploaded file; count lines
        linecount = 0
        while True:
            line = fileitem.file.readline()
            if not line: break
            linecount = linecount + 1
            try:
                #print(line.decode("utf-8", errors="ignore"), "</br>")
                u = line.decode("utf-8")
                #s = u.encode("utf-8")
                print(u)
            except Exception:
                print (Exception)
        
         

except KeyError:
    print ("No such form field ", "name")




fff = open ("txtdoc.txt","r", encoding="utf-8")
print (fff.readline())
     
 

      
print ("</body> </html>")
