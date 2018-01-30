# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 11:15:57 2018

@author: jc

机车监控装置公里标信息和GPS经纬度信息双重定位。日期、时间、车次、弓位、机车型号、机车交路、车站代码、公里标、经纬度、检测值信息叠加视频中，准确定位缺陷点，并自动记录。
"""
import sys
import os
from PyQt5.QtWidgets import ( QMainWindow,QMessageBox)
#重点和秘诀就在这里，大家注意看
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QIcon

import serial
import threading
import time
import struct 

str0='00000'
checi='C1234'
jichexinghao='c2345'
chezhandaima='z1234'
gongwei=12
jichejiaolu = 230
gonglibiao = 200
lat = 0x003CDFBA
lng = 0x00B17DD8
m_port = 'com3'


mmm=[]
threadrun_flag = 1
run_flag = 0
delay_ms = 0.01
BaudRate = 115200
xxx = serial.Serial()

def calcadd(buff,length):
    check = 0
    jj = 2
 
    while jj < length:
        check += buff[jj]
        jj+=1
        
    check = check & 0xff
    #print('%x'%check)
    return check

def init_serial():
    global xxx
    global BaudRate
    global m_port
    xxx.port = m_port
    xxx.baudrate = BaudRate
    xxx.bytesize = 8
    xxx.stopbits = 1
    xxx.parity = serial.PARITY_NONE    


def fasong():
    global xxx
    global threadrun_flag
    global run_flag
    global mmm
    global delay_ms
    global gonglibiao
    global lat
    global lng
    ms =0
    mmm_len = 0
    index = 0
    data_change_count = 0

    try:
        
        while threadrun_flag:
            
            if 0 == run_flag :
                time.sleep(0.5)
                print('**')
                continue
            
            ms = 0
            mmm_len =0
            index =0
            data_change_count = 0
        
            init_serial()
            xxx.open()
            if xxx.isOpen() == True:
                print('open')
            
            while (run_flag & threadrun_flag):
                mmm_len = 0
                ms = int(round(time.time()*1000))
                mmm_len += 3
                mmm[mmm_len]=(ms&0xff)
                mmm_len += 1        
                mmm[mmm_len]=(ms>>8&0xff)
                mmm_len += 1        
                mmm[mmm_len]=(ms>>16&0xff)
                mmm_len += 1        
                mmm[mmm_len]=(ms>>24&0xff)
                mmm_len += 1        
                mmm[mmm_len]=(ms>>32&0xff)
                mmm_len += 1        
                mmm[mmm_len]=(ms>>40&0xff)
                mmm_len += 1        
          
                for index in range(0,len(checi)):
                    mmm[mmm_len] = ord(checi[index])
                    mmm_len += 1 
                
                
                mmm[mmm_len] = gongwei&0xff
                mmm_len += 1         
                mmm[mmm_len] = gongwei>>8&0xff
                mmm_len += 1         
                
                for index in range(0,len(jichexinghao)):
                    mmm[mmm_len] = ord(jichexinghao[index])
                    mmm_len += 1           
                       
                    
                mmm[mmm_len] = jichejiaolu&0xff
                mmm_len += 1         
                mmm[mmm_len] = jichejiaolu>>8&0xff
                mmm_len += 1         
                mmm[mmm_len] = jichejiaolu>>16&0xff
                mmm_len += 1          
                
                for index in range(0,len(chezhandaima)):
                    mmm[mmm_len] = ord(chezhandaima[index])      
                    mmm_len += 1   
                
                mmm[mmm_len] = gonglibiao&0xff
                mmm_len += 1
                mmm[mmm_len] = gonglibiao>>8&0xff
                mmm_len += 1 
                
                mmm[mmm_len]=(lng&0xff)
                mmm_len += 1        
                mmm[mmm_len]=(lng>>8&0xff)
                mmm_len += 1        
                mmm[mmm_len]=(lng>>16&0xff)
                mmm_len += 1        
                mmm[mmm_len]=(lng>>24&0xff)
                mmm_len += 1         
                
                mmm[mmm_len]=(lat&0xff)
                mmm_len += 1        
                mmm[mmm_len]=(lat>>8&0xff)
                mmm_len += 1        
                mmm[mmm_len]=(lat>>16&0xff)
                mmm_len += 1        
                mmm[mmm_len]=(lat>>24&0xff)
                mmm_len += 1        
         
                mmm[mmm_len] = calcadd(mmm,mmm_len)
                mmm_len += 1         
                
                str1 = struct.pack('%dB'%(len(mmm)),*mmm)    
                xxx.write(str1)
         
                time.sleep(delay_ms)
                data_change_count+=1
                if data_change_count >= 3000:
                    gonglibiao +=1
                    if gonglibiao >= 0xffff:
                        gonglibiao = 1
                    
                    lat += 1
                    if lat >= 0xffffffff:
                        lat = 1
                    
                    lng += 1
                    if lng >= 0xffffffff:
                        lng = 1
                        
                    data_change_count = 0
                   
            xxx.close()
            time.sleep(1)
            if xxx.isOpen() != True:
                print('close')
               
    finally:
        xxx.close()
        if xxx.isOpen() != True:
            print('close')

def jieshou():
    myout=""
    while True:
       while xxx.inWaiting()>0:
           myout+=xxx.read(1).decode()
       if myout!="":
            print(myout)
            myout=""
       #myout=x.read(14)
      # myout="lll"
       #time.sleep(1)



class Login(QMainWindow):
    """登录窗口"""
    global checi 
    global jichexinghao 
    global chezhandaima 
    global gongwei 
    global jichejiaolu 
    global gonglibiao
    global lat
    global lng
    global m_port
    def __init__(self, *args):
        super(Login, self).__init__(*args)
        
        if getattr(sys,'frozen',False):
            bundle_dir = sys._MEIPASS
        else:
            bundle_dir = os.path.dirname(os.path.abspath(__file__))
        loadUi(bundle_dir+'\SerialComm.ui', self)   #看到没，瞪大眼睛看
        self.setWindowIcon(QIcon(bundle_dir+'\ha32.ico'))
               
        self.sendBtn.clicked.connect(self.slotSend)
        self.stopBtn.clicked.connect(self.slotStop)
       
    def slotSend(self):
        global run_flag
        global delay_ms
        global BaudRate
        global m_port
        self.sendBtn.setEnabled(False)
        self.checiEdit.setEnabled(False)
        self.gongweiEdit.setEnabled(False)
        self.jichexinghaoEdit.setEnabled(False)
        self.jichejiaoluEdit.setEnabled(False)
        self.chezhandaimaEdit.setEnabled(False)
        self.mscomboBox.setEnabled(False)
        self.gonglibiaoEdit.setEnabled(False)
        self.latEdit.setEnabled(False)
        self.lngEdit.setEnabled(False)  
        self.portcomboBox.setEnabled(False)
        self.mscomboBox.setEnabled(False)
        self.bautecomboBox.setEnabled(False)
        
        self.stopBtn.setEnabled(True)
        
        m_port = self.portcomboBox.currentText()
        
        baute = int(self.bautecomboBox.currentText())
        if 115200 == baute:
            BaudRate = 115200
        elif 9600 == baute:
            BaudRate = 9600
        
        combodata = int(self.mscomboBox.currentText())
        print(combodata)
        if 10 == combodata:
            delay_ms = 0.01
        elif 20 == combodata:
            delay_ms = 0.05
        elif 100 == combodata:
            delay_ms = 0.1
        elif 1000 == combodata:
            delay_ms = 1
        
        if self.checiEdit.toPlainText() == '':
            pass
        else:
            if len(self.checiEdit.toPlainText()) > 5:
                checi = self.checiEdit.toPlainText()[0:5]
            elif len(self.checiEdit.toPlainText()) < 5:
                checi = str0[0:5-len(self.checiEdit.toPlainText())]+self.checiEdit.toPlainText()
            else:
                checi = self.checiEdit.toPlainText()
                
        if self.jichexinghaoEdit.toPlainText() == '':
            pass
        else:
            if len(self.jichexinghaoEdit.toPlainText()) > 5:
                jichexinghao = self.jichexinghaoEdit.toPlainText()[0:5]
            elif len(self.jichexinghaoEdit.toPlainText()) <5 :
                jichexinghao = str0[0:5-len(self.jichexinghaoEdit.toPlainText())]+self.jichexinghaoEdit.toPlainText()
            else:
                jichexinghao = self.jichexinghaoEdit.toPlainText()                
                
        if self.chezhandaimaEdit.toPlainText() == '':
            pass
        else:
            if len(self.chezhandaimaEdit.toPlainText()) > 5:
                chezhandaima = self.chezhandaimaEdit.toPlainText()[0:5]
            elif len(self.chezhandaimaEdit.toPlainText()) < 5:
                chezhandaima = str0[0:5-len(self.chezhandaimaEdit.toPlainText())]+self.chezhandaimaEdit.toPlainText()
            else:
                chezhandaima = self.chezhandaimaEdit.toPlainText()                 
                
        if int(self.gongweiEdit.toPlainText()) == 0:
            pass
        else:
            if int(self.gongweiEdit.toPlainText()) > 65535:
                gongwei = 65535
            else:
                gongwei = int(self.gongweiEdit.toPlainText())              
 
        if int(self.jichejiaoluEdit.toPlainText()) == 0:
            pass
        else:
            if int(self.jichejiaoluEdit.toPlainText()) > 0xffffff:
                jichejiaolu = 0xffffff
            else:
                jichejiaolu = int(self.jichejiaoluEdit.toPlainText())    
        
        if (int(self.gonglibiaoEdit.toPlainText()) >=0) and (int(self.gonglibiaoEdit.toPlainText()) <= 0xffff):
            gonglibiao = int(self.gonglibiaoEdit.toPlainText())
            
        if (int(self.latEdit.toPlainText()) >=0) and (int(self.latEdit.toPlainText()) <= 0xffffffff):
            lat = int(self.latEdit.toPlainText())
            
        if (int(self.lngEdit.toPlainText()) >=0) and (int(self.lngEdit.toPlainText()) <= 0xffffffff):
            lng = int(self.lngEdit.toPlainText())            
        print(checi,jichexinghao,chezhandaima)
        run_flag = 1        

    def slotStop(self): 
        global run_flag
        run_flag = 0
        self.sendBtn.setEnabled(True)
        self.checiEdit.setEnabled(True)
        self.gongweiEdit.setEnabled(True)
        self.jichexinghaoEdit.setEnabled(True)
        self.jichejiaoluEdit.setEnabled(True)
        self.chezhandaimaEdit.setEnabled(True) 
        self.gonglibiaoEdit.setEnabled(True)
        self.latEdit.setEnabled(True)
        self.lngEdit.setEnabled(True)   
        self.portcomboBox.setEnabled(True)
        self.mscomboBox.setEnabled(True)
        self.bautecomboBox.setEnabled(True)
 
        
    def closeEvent(self,event):
        global threadrun_flag
        threadrun_flag = 0
        time.sleep(2)        
 
 
class myThread (threading.Thread):
    def __init__(self,threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID   
    def run(self):
        fasong()    
    


if __name__== '__main__':
    
    mmm = [0]*40
    mmm[0]=0xEB
    mmm[1]=0x90
    mmm[2]=0x24
    
    print(len(mmm))

    app = QApplication(sys.argv)
    login = Login()
    t2 = myThread(1)   #t2= threading.Thread(target=fasong, name="fasong")
    t2.setDaemon(True)
    t2.start()
    login.show()    
    sys.exit(app.exec())  
    
    
    ####################

 
      

 
      
 
 