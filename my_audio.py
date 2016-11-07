# coding=utf8
import os
import re
import wave
import matplotlib.pyplot as plt
import numpy as np


class voice():
    def loaddata(self, filepath):
        '''

        :param filepath: 文件路径，为wav文件
        :return: 如果无异常则返回True，如果有异常退出并返回False
        self.wave_data内储存着多通道的音频数据，其中self.wave_data[0]代表第一通道
        具体有几通道，看self.nchannels
        '''
        if type(filepath) != str:
            print 'the type of filepath must be string'
            return False
        p1 = re.compile('\.wav')
        if p1.findall(filepath) is None:
            print 'the suffix of file must be .wav'
            return False
        try:
            f = wave.open(filepath, 'rb')
            params = f.getparams()
            self.nchannels, self.sampwidth, self.framerate, self.nframes = params[:4]
            str_data = f.readframes(self.nframes)
            self.wave_data = np.fromstring(str_data, dtype=np.short)
            self.wave_data.shape = -1, self.sampwidth
            self.wave_data = self.wave_data.T
            f.close()
            self.name = os.path.basename(filepath)  # 记录下文件名
            return True
        except:
            print 'File Error!'

    def fft(self, frames=40):
        '''
        :param frames: frames是指定每秒钟分块数
        :return:
        '''
        blocks = []
        self.high_point = []
        blocks_size = self.framerate / frames  # block_size为每一块的frame数量
        blocks_num = self.nframes / blocks_size  # 将音频分块的数量
        for i in xrange(blocks_num - 1):
            blocks.append(np.abs(np.fft.fft(self.wave_data[0][i:i + blocks_size])))  #
            self.high_point.append(
                (np.argmax(blocks[i][10:20]) + 10,
                 np.argmax(blocks[i][20:30]) + 20,
                 np.argmax(blocks[i][30:40]) + 30,
                 np.argmax(blocks[i][40:50]) + 40,
                 np.argmax(blocks[i][50:60]) + 50,
                 np.argmax(blocks[i][60:70]) + 60,
                 np.argmax(blocks[i][70:80]) + 70,
                 np.argmax(blocks[i][80:90]) + 80,
                 np.argmax(blocks[i][90:100]) + 90,
                 np.argmax(blocks[i][100:110]) + 100,
                 np.argmax(blocks[i][110:120]) + 110,
                 np.argmax(blocks[i][120:130]) + 120,
                 np.argmax(blocks[i][130:140]) + 130,
                 np.argmax(blocks[i][140:150]) + 140,
                 np.argmax(blocks[i][150:160]) + 150,
                 np.argmax(blocks[i][160:170]) + 160,
                 np.argmax(blocks[i][170:180]) + 170,
                 np.argmax(blocks[i][180:190]) + 180,
                 np.argmax(blocks[i][190:200]) + 190,
                 np.argmax(blocks[i][200:210]) + 200,
                 np.argmax(blocks[i][210:300]) + 210)
            )
        # print len(self.high_point)
            temp_list = []
            for j in range(len(self.high_point[-1])):
                temp_list.append((blocks[i][self.high_point[-1][j]], j))
            temp_list = sorted(temp_list,key=lambda x:x[0])
            for j in range(len(temp_list)):
                temp_list[j] = temp_list[j][1]
            self.high_point[-1] = temp_list
            # high_point存储着fft之后在每个频段的峰值点，存储对象为元组
        # res = []
        # tmp = None
        # for m in self.high_point:
        #     if m != tmp:
        #         tmp=m
        #         res.append(m)
        # self.high_point = res

if __name__ == '__main__':
    p = voice()

    p.loaddata('record_beiyiwang.wav')
    p.fft()
    print p.name
