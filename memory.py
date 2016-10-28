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
        # cur.execute("insert into song_finger VALUES ('%s',NULL)" % tuple_result[0].__str__())
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
    @staticmethod
    def compare(a,b):
        if a[1] > b[1]:
            return True
        else:
            return False
    def simple_search(self, finger_print):
        '''

        :param finger_print: 音频提取出的指纹
        :return:
        '''
        try:
            conn = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db,
                                   charset='utf8')
        except:
            print 'DataBase error'
            return None
        cur = conn.cursor()
        # cur.execute("select * from fp WHERE ")
        song_find_times_dic = {}
        song_find_times_list = []
        for i in finger_print:
            search_str = i[0].__str__()
            cur.execute("select * from fingerprint.fp WHERE fingerprint = '%s'" % search_str)
            point_loc = cur.fetchone()[1]
            temp = point_loc.split(';')[:-1]
            for j in temp:
                find_id = j.split(' ')[0]
                if song_find_times_dic.has_key(find_id):
                    song_find_times_dic[find_id] += 1
                else:
                    song_find_times_dic[find_id] = 1
        for i in song_find_times_dic.keys():
            song_find_times_list.append((i,song_find_times_dic[i]))
        song_find_times_list.sort(cmp=self.compare)
        print song_find_times_list


if __name__ == '__main__':
    v = my_audio.voice()
    v.loaddata('s:\\song\\1.wav')
    v.fft()
    sss = memory('localhost', 3306, 'root', 'root', 'fingerprint')
    # sss.AddNewSong('1.wav')
    for i in range(1,14):
        sss.AddNewSong('s:\\song\\'+i.__str__()+'.wav')
    sss.simple_search(v.hashlist)
