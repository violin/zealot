#!/usr/bin/python
# -*- coding: utf-8 -*-  

import web
import db
import json
import sys,os
from datetime import *
#import openid
import tempfile
import ConfigParser
from whitelist import *
reload(sys)
sys.setdefaultencoding('utf8')

urls = (
    '/', 'index',
    '/json/(.*)/', 'DataProvider',
    '/auth/?(.*)', 'AuthProvider',
    '/static/(.*)', 'StaticProvider',
    '/query', 'QueryProvider',
    '/showCreate', 'TableMetaProvider'
)
app = web.application(urls, globals())
root = tempfile.mkdtemp()
if web.config.get('_session') is None:
     session = web.session.Session(app, web.session.DiskStore(root),initializer={'fullname':''})
     web.config._session = session
else:
     session = web.config._session
     
# 全局变量     
tables = []
configParsed=False

#处理参数

if not configParsed and len(sys.argv) >3 and sys.argv[2].find("config:") >=0 and sys.argv[3].find("target:") >=0:
    global db_host,db_port,db_user,db_passwd,db_database,need_login,target
    configFileName=sys.argv[2][8:]
    target=sys.argv[3][8:]
    print "use config:"+ configFileName
    cf=ConfigParser.ConfigParser()
    cf.read(configFileName)
    db_host=cf.get(target,"db_host")
    db_port=int(cf.get(target,"db_port"))
    db_user=cf.get(target,"db_user")
    db_passwd=cf.get(target,"db_passwd")
    db_database=cf.get(target,"db_database")
    need_login=cf.get(target,"need_login") == 'true' or cf.get(target,"need_login") == 'True'
    configParsed = True
else:
    print '''
        usage: python server.py [port] -config:[configfile] -target:[target]
    '''
    sys.exit(-1)
    
class QueryProvider:
    def POST(self):
        data = web.input()
        print data.condition
        if data.queryType == 'where':
            values = db.queryAll(data.tableName, data.condition, data.orderCondition)
            cols = db.getColumns(data.tableName)
        elif data.queryType == 'full':
            cols = []
            values = db.execQuery(data.condition)
        returnMap = {"v":values,"k":cols}
        return json.dumps(returnMap,cls=CJsonEncoder)
    def GET(self,param):
        return param

class TableMetaProvider:
    def POST(self):
        data = web.input()
        result = db.execQuery("show create table "+ data.tableName)
        return json.dumps(result)
    def GET(self,param):
        return param

class DataProvider:
    def GET(self,param):
        return param
    
class AuthProvider:
    def GET(self,param):
        url =  web.ctx.env['QUERY_STRING']
        try:
            auth = openid.getAuth(url)
            web.setcookie('fullname',auth['fullname'])
        except Exception,e:
            print "auth error:"+str(e)
        web.redirect("/")

class StaticProvider:
    def GET(self,param):
        return web.seeother('/static/'+param)

class index:
    def GET(self):
        global fullname
        fullname =''
        if need_login and session is not None:
            fullname = web.cookies().get('fullname')
            if fullname is None or fullname=='' or fullname not in whiteList:
                #web.redirect(openid.REDIRECT_URL)
                return "not authed"
            else:
                print 'welcome,'+fullname
        render = web.template.render('html/')
        tables=db.initTables()
        return render.index(tables=tables,fullname=fullname,target=target)

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

if __name__ == "__main__":
    print "1. check encoding..."
    print db.execQuery("show variables like 'character_set_%';")
    print "2. web container starting..."
    app.run()
