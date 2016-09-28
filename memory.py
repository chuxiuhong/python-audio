# coding=utf-8

import os

import MySQLdb


class memory():
    def AddNewSong(self, path):
        basename = os.path.basename(path)
        conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='', db='fingerprint')
        cur = conn.cursor()
        cur.execute("insert into song VALUES(NULL," + basename + ');')


sss = memory()
sss.AddNewSong('C:\data\music\\audio\\audio\\ (1).wav')
