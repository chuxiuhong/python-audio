# coding=utf-8
import os
import re
import wave

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
        if p1.findall(filepath) == None:
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

    def fft(self, frames=50):
        '''
        :param frames: frames是指定每秒钟分块数
        :return:
        '''
        try:
            blocks = []
            self.high_point = []
            blocks_size = self.framerate / frames  # block_size为每一块的frame数量
            blocks_num = self.nframes / blocks_size  # 将音频分块的数量
            for i in xrange(blocks_num - 1):
                blocks.append(np.abs(np.fft.fft(self.wave_data[0][i:i + blocks_size])))  #
            for i in xrange(len(blocks)):
                self.high_point.append(
                    (np.argmax(blocks[i][40:100]), np.argmax(blocks[i][100:160]), np.argmax((blocks[i][160:220])),
                     np.argmax(blocks[i][220:280]), np.argmax(blocks[i][280:340])))
                # high_point存储着fft之后在每个频段的峰值点，存储对象为元组
            self.timelist = []
            for i in xrange(len(blocks)):
                self.timelist.append(blocks_size * i * 1.0 / self.framerate)  # 对每个指纹存储在音频中的时间位置
            self.hashlist = []
            for i in xrange(len(blocks)):
                self.hashlist.append((hash(self.high_point[i]), self.timelist[i]))  # hashlist存储着hash值和时间点的元组
        except:
            print 'data error to fft!'
            return False


p = voice()

p.loaddata('C:\data\music\\audio\\audio\\ (1).wav')
p.fft()
for i in p.hashlist:
    print i
print p.name
