__author__ = 'vasilev_is'

import mysql.connector
from mysql.connector import errorcode

def dbdesc():
    return mysql.connector.connect(user='root', passwd='123',host='localhost', db='MiramisDB')
