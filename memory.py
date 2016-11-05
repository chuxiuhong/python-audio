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

    @staticmethod
    def compare(a, b):
        if a[1] > b[1]:
            return True
        else:
            return False

    def addsong(self, path):
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
        namecount = cur.execute("select * from fingerprint.musicdata WHERE song_name = '%s'" % basename)
        if namecount > 0:
            print 'the song has been record!'
            return None
        v = my_audio.voice()
        v.loaddata(path)
        v.fft()
        cur.execute("insert into fingerprint.musicdata VALUES('%s','%s')" % (basename, v.high_point.__str__()))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def fp_compare(search_fp, match_fp):
        '''

        :param search_fp: 查询指纹
        :param match_fp: 库中指纹
        :return:最大相似值 int
        '''
        if len(search_fp) >= len(match_fp):
            return 0
        max_similar = 0
        search_fp_len = len(search_fp)
        match_fp_len = len(match_fp)
        for i in range(match_fp_len - search_fp_len):
            temp = 0
            for j in range(search_fp_len):
                if match_fp[i+j] == search_fp[j]:
                    temp += 1
            if temp > max_similar:
                max_similar = temp
        return max_similar

    def search(self,path):
        v = my_audio.voice()
        v.loaddata(path)
        v.fft()
        try:
            conn = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db,
                                   charset='utf8')
        except:
            print 'DataBase error'
            return None
        cur = conn.cursor()
        cur.execute("select * from fingerprint.musicdata")
        result = cur.fetchall()
        for i in result:
            memory.fp_compare(v.high_point[100:300],eval(i[1]))
        cur.close()
        conn.close()

if __name__ == '__main__':
    sss = memory('localhost', 3306, 'root', '', 'fingerprint')
    sss.addsong('1.wav')
    sss.search('1.wav')
