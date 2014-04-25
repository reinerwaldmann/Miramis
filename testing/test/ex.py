#!/usr/bin/python3                                                                                                            
                                                                                                                              
import io, cgi, cgitb, sys                                                                                                    
                                                                                                                              
cgitb.enable()                                                                                                                
                                                                                                                              
if hasattr(sys.stdout, "buffer"):                                                                                            
  def bwrite(s):                                                                                                              
    sys.stdout.flush()                                                                                                     
    sys.stdout.buffer.write(s)                                                                                                
  write = sys.stdout.write                                                                                                    
else:                                                                                                                        
  wrapper = io.TextIOWrapper(sys.stdout)                                                                                      
  def bwrite(s):                                                                                                              
    wrapper.flush()                                                                                                          
    sys.stdout.write(s)                                                                                                      
  write = wrapper.write                                                                                                      
                                                                                                                              
write("Content-type: text/html;charset=utf-8\r\n\r\n")                                                                        
                                                                                                                              
bwrite("""<!DOCTYPE html>                                                                                                    
                                                                                                                              
<html>                                                                                                                        
<head>                                                                                                                        
  <title>CGI</title>                                                                                                          
</head>                                                                                                                      
<body>                                                                                                                        
                                                                                                                              
<p>Русский текст.</p>                                                                                                        
                                                                                                                              
</body>                                                                                                                      
</html>""".encode())#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cgitb, cgi, io, sys, os
print ("Content-type: text/html charset: utf-8  \n")
cgitb.enable()  
st="<html> <center> кириллица Hello!  </center></html>"
print (st)


