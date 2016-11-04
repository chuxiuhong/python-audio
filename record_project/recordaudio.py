# coding=utf8
# http://stackoverflow.com/questions/16111038/how-to-convert-pcm-files-to-wav-files-scripting
import os
import sys
import wave

from PyQt4 import QtGui
from PyQt4.QtCore import *
import time
class recorder():
    def __init__(self, sampleframe, bit, channels, ntime):
        self.sampleframe = int(sampleframe)
        self.bit = int(bit)
        self.channels = int(channels)
        self.time = int(ntime)

    def record(self):
        os.system("ConsoleApplication7.exe %s %s %s %s" % (
        self.sampleframe.__str__(), self.bit.__str__(), self.channels.__str__(), self.time.__str__()))
        with open('record.pcm', 'rb') as pcmfile:
            pcmdata = pcmfile.read()
        f = wave.open('record' + '.wav', 'wb')
        f.setparams((self.channels, 2, self.sampleframe, 0, 'NONE', 'NONE'))
        f.writeframes(pcmdata)
        f.close()


class UI(QtGui.QWidget):
    def __init__(self):
        super(UI, self).__init__()
        self.initUI()

    def initUI(self):
        grid = QtGui.QGridLayout()
        self.time = QtGui.QLineEdit()
        self.fre = QtGui.QLineEdit()
        self.bit = QtGui.QLineEdit()
        self.button = QtGui.QPushButton(u'录音')
        self.label1 = QtGui.QLabel(u'请输入采样频率')
        self.label2 = QtGui.QLabel(u'请输入采样比特')
        self.label3 = QtGui.QLabel(u'请输入录音时间')
        self.status = QtGui.QLabel(u'空闲中')
        grid.addWidget(self.fre, 1, 2)
        grid.addWidget(self.bit, 2, 2)
        grid.addWidget(self.time, 3, 2)
        grid.addWidget(self.button, 4, 4)
        grid.addWidget(self.label1, 1, 1)
        grid.addWidget(self.label2, 2, 1)
        grid.addWidget(self.label3, 3, 1)
        grid.addWidget(self.status,4,2)
        self.setLayout(grid)
        self.connect(self.button, SIGNAL("clicked()"), self.record)

    def record(self):
        time.sleep(0.5)
        r = recorder(self.fre.text(), self.bit.text(), 1, self.time.text())
        r.record()
        self.status.setText(u'录音完成')


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ui = UI()
    ui.setWindowTitle(u'我的录音器')
    ui.show()
    app.exec_()
