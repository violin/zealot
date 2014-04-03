import MySQLdb
import config
import json
import decimal


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

def queryAll(tableName,condition='1=1',orderCondition='id desc',start=0,offset=100):
    try:
        if condition == None or len(condition.strip())==0:
            condition='1=1'
        if orderCondition == None or len(orderCondition.strip())==0 or orderCondition== 'null':
            orderCondition='id desc'
        conn=MySQLdb.connect(host=config.db_host,user=config.db_user,passwd=config.db_passwd,port=config.db_port,db=config.db_database)
        cur=conn.cursor()
        query = 'select * from ' + tableName +' where ' + condition +' order by '+orderCondition +' limit ' +str(start) + ','+str(offset)
        print query
        cur.execute(query)
        results=[]
        for row in cur.fetchall():
            newrow = []
            for x in row:
                if isinstance(x, decimal.Decimal):
                    newrow.append(decimal.Decimal.to_eng_string(x))
                else:
                    newrow.append(x)
            results.append(newrow)
        return results
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        cur.close()
        conn.close()

def execQuery(fullQuery):
    try:
        conn=MySQLdb.connect(host=config.db_host,user=config.db_user,passwd=config.db_passwd,port=config.db_port,db=config.db_database)
        cur=conn.cursor()
        print fullQuery
        cur.execute(fullQuery)
        results=[]
        if fullQuery.find('insert')>=0 or fullQuery.find('update')>=0 or fullQuery.find('delete')>=0:
            conn.commit()
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
    print queryAll("moc_test_answerform")