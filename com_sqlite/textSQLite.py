#coding:utf-8
from common import SQLiteDataBase
def getsq():
    db = SQLiteDataBase()
    sql = 'SELECT `id`,`name` FROM student'
    results = db.query(sql)
    print results
getsq()