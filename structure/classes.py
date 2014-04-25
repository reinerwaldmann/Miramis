Python 3.3.2 (v3.3.2:d047928ae3f6, May 16 2013, 00:06:53) [MSC v.1600 64 bit (AMD64)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> 
>>> 
>>> 
>>> tr=[1,["as",2]]
>>> print tr
SyntaxError: invalid syntax
>>> print (tr)
[1, ['as', 2]]
>>> d = {1: {'olol', 'UAZ'}, 2: {'two', 'OMSK'}, 3: {'three', 'Printer'}}
>>> print d
SyntaxError: invalid syntax
>>> print (d)
{1: {'UAZ', 'olol'}, 2: {'two', 'OMSK'}, 3: {'Printer', 'three'}}
>>> print d[1]['olol']
SyntaxError: invalid syntax
>>> print (d[1]['olol']
       )
Traceback (most recent call last):
  File "<pyshell#11>", line 1, in <module>
    print (d[1]['olol']
TypeError: 'set' object is not subscriptable
>>> for val in d.values:
	print (val)

	
Traceback (most recent call last):
  File "<pyshell#14>", line 1, in <module>
    for val in d.values:
TypeError: 'builtin_function_or_method' object is not iterable
>>> gd = {1: {'olol': 'UAZ', 'olol1': 'Volga'}, 2: {'two': 'OMSK'}, 3: {'three': 'Printer'}}
>>> 
>>> 
>>> print (gd)
{1: {'olol1': 'Volga', 'olol': 'UAZ'}, 2: {'two': 'OMSK'}, 3: {'three': 'Printer'}}
>>> for val in gd.values:
	print (val)

	
Traceback (most recent call last):
  File "<pyshell#21>", line 1, in <module>
    for val in gd.values:
TypeError: 'builtin_function_or_method' object is not iterable
>>> for key in gd.keys():
	print (key)

	
1
2
3
>>> for val in gd.values():
	for valval in val.values():
		print (valval)

		
Volga
UAZ
OMSK
Printer
>>> print([key, val, valval for val in gd.values()])
