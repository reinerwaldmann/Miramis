__author__ = 'vasilev_is'
import sys

#генерирует начало HTML-файла
def generateHTMLMetaHeader(title="Протокол испытаний"):
    res="""Content-Type: text/html;charset=utf-8\n\n
    <html lang="ru-RU">
    <head>
    <meta charset="UTF-8" />
    <title> {0}  </title>
    <link rel="stylesheet" type="text/css" media="all" href="main.css" />
    <script type='text/javascript' src='../MiramisPHP/scripts.js'></script>
    </head>
    <body>
    """.format(title)
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