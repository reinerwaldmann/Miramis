#!C:\Python33\python.exe
# -*- coding: utf-8

def wrap(text, width=70, **kwargs):
    from textwrap import TextWrapper
    w=TextWrapper(width=width, **kwargs)
    return w.wrap(text)



def m(*args):
    for i in args:
        print (i)
    return None;

#print (m(2,3,4,5,6))


def sk(a1, *ar, **kw):
        print (a1)
        print (ar)
        print (kw)
        return None

def fuck(**kw):
    #for key in kw:
        #print (key, '\tcorresponds\t', kw[key])
    for key, value in kw.items():
        print (key, value)
    return None

def returntuple ():
    return 101, 304

#a, b = returntuple()
#print (a,'trololo', b)


def appshit (a):
    return a**3

def appshit2 (a):
    return a**4



def appsh2 (a, m):
    return str(m(a))+"fucking";

#print (appsh2(2, appshit2))

#print (list(filter(lambda x: x.isalpha(),'fuckin2k2k2k olo Om2s4k')))


#print ('УПРТСТЬ'+'\tOMSK'+str(222))

#print ([x for x in enumerate("OMSK")])
#print ([x for x in sorted("bdcab123")])


import copy, pickle

class MyClass(object):
     
    def __init__(self, iname=" "):
        self.id=2
        self.name=iname



    def getName(self, prefix):
        return prefix+self.name
     
#представляет объект в виде строки
    def __repr__(self):
        return "id=%s name=%s"%(self.id, self.name)
    


    #для консервации
    def __getinitargs__(self):
        return "UAZ"

  

    

#s=MyClass("UAZ")
#for i, val in s.__dict__.items():
    #print (i, val)


s=MyClass("UAZ")
print (s)


b=copy.deepcopy(s)
print (b)


pickle.dump (b, open("save.txt", "wb"))

h=pickle.load(open("save.txt","rb"))
print (h)
 
 
 
 
    

 

#fuck (a='m', b='l')
#sk(1)
#sk(1,2,3,4,5)
#sk(1,2,3,a='abc', b='sdf')
 
#Возвращаем кортеж

