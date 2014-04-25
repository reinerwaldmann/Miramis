#!/usr/bin/python3                                                                                                            
#-*- coding: utf-8
                                                                                                                              
import io, cgi, cgitb, sys                                                                                                    
                                                                                                                              
cgitb.enable()                                                                                                                
                                                                                                                              
if hasattr(sys.stdout, "buffer"):                                                                                            
  def bwrite(s):                                                                                                              
    sys.stdout.flush()                                                                                                     
    sys.stdout.buffer.write(s)                                                                                                
  write = sys.stdout.write                                                                                                    
else:
    try:
        wrapper = io.TextIOWrapper(sys.stdout)
        def bwrite(s):                                                                                                              
            wrapper.flush()                                                                                                          
            sys.stdout.write(s)                                                                                                      
        write = wrapper.write
    except:
        pass

    
#write("Content-type: text/html;charset=utf-8\r\n\r\n")                                                                        
                                                                                                                              
#bwrite("""<!DOCTYPE html>                                                                                                    
                                                                                                                              
#<html>                                                                                                                        
#<head>                                                                                                                        
  #<title>CGI</title>                                                                                                          
#</head>                                                                                                                      
#<body>                                                                                                                        
                                                                                                                              
#<p>Русский текст.</p>                                                                                                        
                                                                                                                              
#</body>                                                                                                                      
#</html>""".encode())

