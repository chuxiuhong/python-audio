# coding=utf8
import re
import wave

import numpy as np
import pyaudio
import os

class voice():
    def loaddata(self, filepath):
        '''

        :param filepath: 文件路径，为wav文件
        :return: 如果无异常则返回True，如果有异常退出并返回False
        self.wave_data内储存着多通道的音频数据，其中self.wave_data[0]代表第一通道
        具体有几通道，看self.nchannels
        '''
        if type(filepath) != str:
            raise TypeError, 'the type of filepath must be string'
        p1 = re.compile('\.wav')
        if p1.findall(filepath) is None:
            raise IOError, 'the suffix of file must be .wav'
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
            raise IOError, 'File Error'

    def fft(self, frames=40):
        block = []
        self.fft_blocks = []
        #self.high_point = []
        blocks_size = self.framerate / frames  # block_size为每一块的frame数量
        blocks_num = self.nframes / blocks_size  # 将音频分块的数量
        for i in xrange(0, len(self.wave_data[0]) - blocks_size, blocks_size):
            block.append(self.wave_data[0][i:i + blocks_size])
            self.fft_blocks.append(np.abs(np.fft.fft(self.wave_data[0][i:i + blocks_size])))
        print type(self.fft_blocks[0])

    def play(self, filepath):
        '''
        音频播放方法
        :param filepath:文件路径
        :return:
        '''
        chunk = 1024
        wf = wave.open(filepath, 'rb')
        p = pyaudio.PyAudio()
        # 打开声音输出流
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        # 写声音输出流进行播放
        while True:
            data = wf.readframes(chunk)
            if data == "":
                break
            stream.write(data)
        stream.close()
        p.terminate()

if __name__ == '__main__':
    v = voice()
    v.loaddata('C:\\data\\python-audio\\record.wav')
    v.fft()