__author__ = 'vasilev_is'
#генерирует начало HTML-файла
def generateHTMLMetaHeader(title="Протокол испытаний"):
    res="""<!DOCTYPE html>
    <html lang="ru-RU">
    <head>
    <meta charset="UTF-8" />
    <title> {0}  </title>
    <link rel="stylesheet" type="text/css" media="all" href="" />
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
