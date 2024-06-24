import sqlite3
import os
from datetime import time


class Database():

    def __init__(self):
        if not os.path.exists("database.db"):
            self.create_db()

    @staticmethod
    def create_db():
        connect = sqlite3.connect("database.db")
        c = connect.cursor()
        c.execute('''create table IF NOT EXISTS videos (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
            path varchar(1000),
            name varchar(1000),
            duration INTEGER,
            position INTEGER,
            size INTEGER,
            width INTEGER,
            height INTEGER,
            patch varchar(1000),
            subtitles varchar(1000),
            encrypt INTEGER,
            headers varchar(1000),
            create_at TIMESTAMP,
            updated_at TIMESTAMP
        );''')
        c.close()
        connect.close()

    @staticmethod
    def insertData(path,name,duration,position,size,width,height,patch,subtitles,encrypt,headers):
        connect = sqlite3.connect("database.db")
        c = connect.cursor()
        sql = "INSERT INTO videos (path, name, duration, position, size, width,height,patch,subtitles,encrypt,headers,create_at,updated_at) values (?,?,?,?,?,?,?,?,?,?,?)"
        data = (path,name,duration,position,size,width,height,patch,subtitles,encrypt,headers,time(),time())
        c.execute(sql,data)
        connect.commit()
        c.close()
        connect.close()

    def deleteData(self):
        pass

    def editData(self):
        pass
