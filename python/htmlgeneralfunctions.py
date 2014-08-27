#!/usr/bin/python3.4
__author__ = 'vasilev_is'
import sys

#генерирует начало HTML-файла
def generateHTMLMetaHeader(title="Протокол испытаний", displaymenu=1):
    res="""Content-Type: text/html;charset=utf-8\n\n
    <html lang="ru-RU">
    <head>
    <meta charset="UTF-8" />
    <title> {0}  </title>

    <script type='text/javascript' src='../MiramisPHP/scripts.js'></script>
    <script type='text/javascript' src='../MiramisPHP/functions.js'></script>

    </head>
    <body>
    """.format(title)


    #<link rel="stylesheet" type="text/css" media="all" href="http://192.168.111.15/MiramisPHP/main.css" />

    if displaymenu==1:
        res+="<a href='../MiramisPHP/protocols.php'> Обзор протоколов </a> &nbsp&nbsp&nbsp&nbsp <a href='../MiramisPHP/results.php'> Обзор результатов </a>";



    return res





def generateHTMLFooter():
    return """
    </body> </html>
    """
def generateHTMLFooterRep():
    return """ </tbody>
    </table>
    </body> </html>
    """
#добавить подпися, если надо


def throwError(creatorname, errortext, errortype=None):
    return "<script>alert('"+creatorname+": "+errortext+"')</script>"


def out(msg):
    sys.stdout.buffer.write(msg.encode('utf8'))
    sys.stdout.flush()