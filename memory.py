# coding=utf-8

import os

import MySQLdb

import my_audio


class memory():
    def __init__(self, host, port, user, passwd, db):
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
            conn = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db,
                                   charset='utf8')
        except:
            print 'DataBase error'
            return None
        cur = conn.cursor()
        namecount = cur.execute("select * from song WHERE name = '%s'" % basename)
        if namecount > 0:
            print 'the song has been record!'
            return None

        cur.execute("insert into song VALUES(NULL,'%s' );" % basename)
        conn.commit()
        cur.execute("select * from song WHERE  name='%s'" % basename)
        tuple_result = cur.fetchone()  # 存储歌曲的id和name
        #cur.execute("insert into song_finger VALUES ('%s',NULL)" % tuple_result[0].__str__())
        v = my_audio.voice()
        v.loaddata(path)
        v.fft()
        for i in v.hashlist:
            count = cur.execute("select * from fp WHERE fingerprint.fp.fingerprint = '%d'" % i[0])
            if count > 0:
                cur.execute("select * from fp WHERE fingerprint.fp.fingerprint = '%d'" % i[0])
                temp = cur.fetchone()
                id_temp = temp[1] + tuple_result[0].__str__() + ' ' + i[1].__str__() + ';'  # 用来更新的结果，在数据库中是TEXT类型
                # print 'id_temp', id_temp
                cur.execute("UPDATE fingerprint.fp set id = '%s' WHERE fingerprint = '%s'" % (id_temp, temp[0]))
            else:
                # print i[0]id
                # print tuple_result[0].__str__()+' '+ i[1].__str__() + ';'
                cur.execute(
                    "insert into fp VALUES(%d,'%s')" % (i[0], tuple_result[0].__str__() + ' ' + i[1].__str__() + ';'))

        conn.commit()
        cur.close()
        conn.close()

    def search(self, finger_print):
        '''

        :param finger_print: 音频提取出的指纹
        :return:
        '''


sss = memory('localhost', 3306, 'root', '', 'fingerprint')
sss.AddNewSong('C:\data\music\\audio\\audio\\ (2).wav')
