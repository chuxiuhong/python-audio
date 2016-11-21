# coding=utf8
import os
import re
import wave

import numpy as np
import pyaudio


class voice():
    def loaddata(self, filepath):
        '''

        :param filepath: 文件路径，为wav文件
        :return: 如果无异常则返回True，如果有异常退出并返回False
        self.wave_data内储存着多通道的音频数据，其中self.wave_data[0]代表第一通道
        具体有几通道，看self.nchannels
        '''
        if type(filepath) != str:
            raise TypeError,'the type of filepath must be string'
        p1 = re.compile('\.wav')
        if p1.findall(filepath) is None:
            raise IOError,'the suffix of file must be .wav'
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
        block = []
        fft_blocks = []
        self.high_point = []
        blocks_size = self.framerate / frames  # block_size为每一块的frame数量
        blocks_num = self.nframes / blocks_size  # 将音频分块的数量
        for i in xrange(0, len(self.wave_data[0]) - blocks_size, blocks_size):
            block.append(self.wave_data[0][i:i + blocks_size])
            fft_blocks.append(np.abs(np.fft.fft(self.wave_data[0][i:i + blocks_size])))
            self.high_point.append((np.argmax(fft_blocks[-1][:40]),
                                    np.argmax(fft_blocks[-1][40:80]) + 40,
                                    np.argmax(fft_blocks[-1][80:120]) + 80,
                                    np.argmax(fft_blocks[-1][120:180]) + 120,
                                    # np.argmax(fft_blocks[-1][180:300]) + 180,
                                    ))
            '''
            temp_list = []
            for j in range(len(self.high_point[-1])):
                temp_list.append((fft_blocks[-1][self.high_point[-1][j]], j))
            temp_list = sorted(temp_list, key=lambda x: x[0])
            for j in range(len(temp_list)):
                temp_list[j] = temp_list[j][1]
            #print temp_list
            self.high_point[-1] = temp_list
            '''

    def play(self, filepath):
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
            if data == "": break
            stream.write(data)

        stream.close()
        p.terminate()


if __name__ == '__main__':
    p = voice()

    p.play('the_mess.wav')
    print p.name
