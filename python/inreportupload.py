#!/usr/bin/python3.4
#!/usr/bin/python3.4
#!/usr/bin/python3.4
#!/usr/bin/python3.4
#!/usr/bin/python3.4
from python.classes import AProtocol

__author__ = 'vasilev_is'

from python.parsers import *
import backend_manageProtocols as bck

import pickle

from mydbconnect import dbdesc


def upload_to_protocol(filedescriptor):
    """
    Загружает протокол из файла в базу данных. Пока через Pickle
    """

    bck.writeProtocolToDatabase(parseToAProtocol(filedescriptor))



#debugging procedures
def test ():
    """
    for debugging
    """
    filename="sandbox/protocolCP1251.txt"

# import platform
# #print (platform.system())
#
# if (platform.system().__contains__("Linux")):
#     filename="utf8.txt" #и вот тут должно быть перекодирование, тащемта
# else:

    try:
        file=open(filename, "r")
    except:
        print("Error while opening file")
        return
    upload_to_protocol(file)

test()



