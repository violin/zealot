import MySQLdb
import config
import json


def initTables(): 
    try:
        conn=MySQLdb.connect(host=config.db_host,user=config.db_user,passwd=config.db_passwd,port=config.db_port,db=config.db_database)

        cur=conn.cursor()
        cur.execute('show tables;')
        rows=[]
        for row in cur.fetchall():
            rows.append(row[0])
        return rows
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        cur.close()
        conn.close()

def queryAll(tableName,condition='1=1',start=0,offset=100):
    try:
        if condition == None or len(condition.strip())==0:
            condition='1=1'
        conn=MySQLdb.connect(host=config.db_host,user=config.db_user,passwd=config.db_passwd,port=config.db_port,db=config.db_database)
        cur=conn.cursor()
        query = 'select * from ' + tableName +' where ' + condition +' limit ' +str(start) + ','+str(offset)
        print query
        cur.execute(query)
        results=[]
        for row in cur.fetchall():
            results.append(row)
        return results
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        cur.close()
        conn.close()

def getColumns(tableName):
    try:
        conn=MySQLdb.connect(host=config.db_host,user=config.db_user,passwd=config.db_passwd,port=config.db_port,db=config.db_database)
        cur=conn.cursor()
        query = 'show create table ' + tableName 
        print query
        cur.execute(query)
        results=[]
        for row in cur.fetchall():
            results.append(row)
        jsonstr = json.dumps(results)
        cols =  jsonstr.split('\\n')
        for i in range(0,len(cols)):
            if cols[i].find('KEY') >=0:
                endIndex = i
                break
        unparsed = cols[1:endIndex]   
        returnList = [] 
        for n in unparsed:
            returnList.append(n.strip().split(' ')[0][1:-1]) 
        return returnList
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        cur.close()
        conn.close()


if __name__ == '__main__':
    tables = initTables()
    rows = getColumns(tables[0])
    # print rows
    for x in rows:
        print x
    # for x in range(0,len(rows.split('\n'))) 
    #     println rows.split('\n')[x]