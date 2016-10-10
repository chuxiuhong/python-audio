# coding=utf-8

import os

import MySQLdb
import pyaudio

class memory():
    def __init__(self,host,port,user,passwd,db):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
    def AddNewSong(self, path):
        if type(path) != str:
            print 'path need string'
            return None
        basename = os.path.basename(path)
        try:
            conn = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db,charset='utf8')
        except:
            print 'DataBase error'
            return None
        cur = conn.cursor()
        namecount = cur.execute("select * from song WHERE name = '%s'" % basename)
        if namecount > 0:
            print 'the song has been record!'
            return None

        cur.execute("insert into song VALUES(NULL,'%s' );"%basename)
        conn.commit()
        cur.execute("select * from song WHERE  name='%s'"%basename)
        tuple_result = cur.fetchone()#存储歌曲的id和name
        v = pyaudio.voice()
        v.loaddata(path)
        v.fft()
        for i in v.hashlist:
            count = cur.execute("select * from fp WHERE fingerprint.fp.fingerprint = '%d'"%i[0])
            if count > 0:
                cur.execute("select * from fp WHERE fingerprint.fp.fingerprint = '%d'" % i[0])
                temp = cur.fetchone()
                id_temp = temp[1] +tuple_result[0].__str__()+ ' ' + i[1].__str__() + ';'
                print 'id_temp', id_temp
                cur.execute("UPDATE fingerprint.fp set id = '%s' WHERE fingerprint = '%s'"%(id_temp,temp[0]))
            else:
                # print i[0]
                # print tuple_result[0].__str__()+' '+ i[1].__str__() + ';'
                cur.execute("insert into fp VALUES(%d,'%s')"%(i[0],tuple_result[0].__str__()+' '+ i[1].__str__() + ';'))
        conn.commit()
        cur.close()
        conn.close()


sss = memory('localhost', 3306,'root','','fingerprint')
sss.AddNewSong('C:\data\music\\audio\\audio\\ (2).wav')
