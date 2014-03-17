#!/usr/bin/python
#coding=utf-8   

import web
import db
import json

urls = (
    '/', 'index',
    '/json/(.*)/', 'DataProvider',
    '/static/(.*)', 'StaticProvider',
    '/query', 'QueryProvider'
)
tables = []

class QueryProvider:
    def POST(self):
        data = web.input()
        print data.condition
        values = db.queryAll(data.tableName, data.condition)
        cols = db.getColumns(data.tableName)
        returnMap = {"v":values,"k":cols}
        return json.dumps(returnMap)
    def GET(self,param):
        return param

class DataProvider:
    def GET(self,param):
        return param

class StaticProvider:
    def GET(self,param):
        return web.seeother('/static/'+param)

class index:
    def GET(self):
        render = web.template.render('html/')
        tables=db.initTables()
        return render.index(tables)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
