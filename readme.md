## zealot

### introduction
this is a project for database basic access, with connections to netease ddb 4.5.6 , and standard Mysql 5.6.

to startup, execute: 
```
python server.py [port] -config:config/config.ini -target:some-target
```
whitelist.py is used for privilege ,which is now implemented with plain text fullname. future work: import encryption.

`config/config.ini` is used for database connection configuration, which is clear enough.  

in server.py I have already implemented auth function, but I removed openid.py module for sake of protection of company sensitive info. other similar extention can be added as `AuthProvider` does.

### dependency
> python, webpy, MySQLdb(with pip,easy_install or install manually)

### release notes:
- v1.0:  base interface , view layer ,infrastructure, db query
- v2.0:  db insert,update, table structure showing
- v3.0:  whitelist, startup configurably.

### GUI
data showing
![data showing](http://www.pyhero.com/image_store/zealot1.png).

data edit
![data edit](http://www.pyhero.com/image_store/zealot2.png).



