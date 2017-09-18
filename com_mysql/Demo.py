#coding:utf-8
from common.Database import Database
def getData():
    db = Database()
    sql = 'SELECT * FROM douban'
    results = db.query(sql)
    return results
for i in getData():
    print i[2],i[3]