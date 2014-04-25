#!C:\Python33\python.exe
# -*- coding: utf-8
import mysql.connector
from mysql.connector import errorcode

 


print("Content-Type: text/html;charset=utf-8")
print() # <----------- addtional newlnie for header/body separation.
print ("<html><head>")
print() # <----------- addtional newlnie for header/body separation.
print ("</head><body>")
print ("At least python is working now!!")

#mysql

try:
    con=mysql.connector.connect(user='root', passwd='1234',host='localhost', db='test1')

    cursor=con.cursor()
    query=("select id_city, name  from city;")
    cursor.execute(query)

 
    for (id_city, name) in cursor:
        print(name)
    
    cursor.close()
    con.close()
    
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exists")
  else:
      print(err)
else:
    con.close()

#http://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
    
#http://webonrails.ru/post/490/

print ("</body></html>")
