# coding=utf-8

import os

import MySQLdb


class memory():
    def AddNewSong(self, path):
        basename = os.path.basename(path)
        print basename
        conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='', db='fingerprint')
        cur = conn.cursor()
        cur.execute("insert into song VALUES(NULL,123);")
        conn.commit()
        cur.close()
        conn.close()

sss = memory()
sss.AddNewSong('output2.wav')
