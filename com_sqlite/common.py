# coding=utf-8
import sqlite3
class SQLiteDataBase:

    def __init__(self):
        self.db = sqlite3.connect("mysite.db")
        self.cursor = self.db.cursor()

    def query(self, sql):
        self.cursor.execute(sql)
        self.db.commit()
        results = self.cursor.fetchall()
        return results

    def execute(self, sql):
        self.cursor.execute(sql)
        self.db.commit()
        return 1

    def __del__(self):
        self.db.close()
