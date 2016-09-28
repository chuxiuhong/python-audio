#coding=utf-8

import MySQLdb

class memory():
    def AddNewSong(self,path,):
        conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='', db='fingerprint')
        cur = conn.cursor()
        cur.execute()