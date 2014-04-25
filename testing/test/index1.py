#!C:\Python34\python.exe
#-*- coding: utf-8

                                                                                                                              
import io, cgi, cgitb, sys                                                                                                    
#sys.stdout._encoding = 'utf-8'

def out(msg):
    sys.stdout.buffer.write(msg.encode('utf8'))
    sys.stdout.flush()




out("Content-Type: text/html;charset=utf-8\n\n")
out("<html><head>\n\n")
out("</head><body>\n\n")


#sys.stdout.buffer.write(b'Content-type: text/html;charset=utf-8\n\n')
 

# test

 
out("кириллица")




print ("</body> </html>")
