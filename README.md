# simple dmidecode
If you're like me, and I know I am, part of your job involves doing things on, near, or to servers. One of the better
tools out there for getting information about your server is dmidecode, the handy program that decodes a system's
Desktop Management Interface information...most of which is totally useless to you. Sadly, recognition of that last
bit is missing in the existing Python dmidecode modules, so it is with a modest amount of fanfare that I introduce
simple_dmidecode.  Simple_dmidecode throws out tons of functionality in favor of doing things that are actually useful
to most system administrators. Dmidecode already supports this approach in their 22 core keywords...and those core
keywords are exactly what simple_dmidecode supports.  Those and nothing else. Want something else?  Use something else.

##Usage:
###Return a dict containing the dmidecode outputs
```
from simple_dmidecode import Dmi
a = Dmi()
myhostinfo = a.decode()
```
###Dump a JSON of the same dict
```
myhostinfo = a.decode()
try:
  open("mydmi.json", "w")
  a.dumpjson("w")
finally:
  close("mydmi.json")
```
If no filehandle is passed to dumpjson(), the output will be sent to sys.stdout.
If "None" is passed to dumpjson(), no output will be printed.
The method returns a string containing the JSON-formatted data.
###Dump an XML of the dict
```
myhostinfo = a.decode()
try:
  open("mydmi.xml", "w")
  a.dumpxml("w")
finally:
  close("mydmi.xml")
```
As with JSON, if no filehandle is passed, the output is prettified with xml.dom.minidom and printed to sys.stdout.
If "None" is passed as the filehandle, no printed output is produced.
The method returns an xml.etree.ElementTree.ElementTree object containing the constructed data.
Please be aware that xml.etree.ElementTree is vulnerable to a number of anti-XML parser attacks.  Program accordingly.
###SQL constructor
```
myhostinfo = a.decode()
myinsertsql = a.dumpsql("MYTABLE", "MY_PK", THIS_PKVALUE, "INSERT", list_of_keys_i_want)
myupdatesql = a.dumpsql("MYTABLE", "MY_PK", THIS_PKVALUE, "UPDATE", list_of_keys_i_want)
```
Basic SQL INSERT/UPDATE constructor. If you give it a table, a primary key column and value, a mode (INSERT or UPDATE)
and (optionally) a list containing the keywords you want it to pull for you, it will return a string containing
reasonably well-formatted SQL to insert or update that row.
It is left as an exercise for the user to validate that SQL, make sure it doesn't do something horrible, etc.
##TODO:
* Move dmidecode path discovery out of __init__ and replace with hardcoded /usr/sbin; add new method to run path discovery.
