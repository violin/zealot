#!/usr/bin/python
# -*- coding: utf-8 -*-  

import web
import db
import json
import sys,os
import openid
import tempfile
from openid import REDIRECT_URL
from compiler.pycodegen import EXCEPT
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
tables = []

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
        return json.dumps(returnMap)
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
            session['fullname']=auth['fullname']
        except Exception,e:
            print "auth error:"+e
        web.redirect("/")

class StaticProvider:
    def GET(self,param):
        return web.seeother('/static/'+param)

class index:
    def GET(self):
        fullname = session['fullname'] 
        if session is not None:
            if fullname== '':
                web.redirect(REDIRECT_URL)
            else:
                print 'welcome,'+fullname
        render = web.template.render('html/')
        tables=db.initTables()
        return render.index(tables=tables,fullname=fullname)


if __name__ == "__main__":
    app.run()
