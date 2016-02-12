#simple_dmidecode
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
try:
  open("myjsonfile", "w")
  a.dumpjson("w")
finally:
  close("myjsonfile")
```
##TODO:
* Add more output modes.
* XML coming soon.
* Move dmidecode path discovery out of __init__ and replace with hardcoded common RHEL/CentOS path + new method to run path discovery.
* Add support for output of std. SQL.
