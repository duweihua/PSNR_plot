# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import MultipleLocator, FuncFormatter
#from multiprocessing import Process
import threading
from time import ctime,sleep
import struct
import math
import sys

MultipleLocator.MAXTICKS = 1000
FRAME_NUM=600

fig=plt.figure(figsize=(15,9))
# 设置图的底边距
plt.subplots_adjust(top=0.98)
plt.subplots_adjust(bottom=0.05)
plt.subplots_adjust(left=0.08)
plt.subplots_adjust(right=0.97)


x_plt=np.arange(0,FRAME_NUM,1)
############################### #### #####
############################### SPNR #####
ax_psnr = fig.add_subplot(211)
plt.sca(ax_psnr) #set active fig
## plt.plot(x, y1[0:300], label='PSNR', color='red') #描点
# 设置sub1 两个坐标轴的范围
plt.xlim(0,FRAME_NUM)
plt.ylim(35,45)
plt.grid() #开启网格#
# 主刻度
ax_psnr.xaxis.set_major_locator( MultipleLocator(30) )
ax_psnr.yaxis.set_major_locator( MultipleLocator(1) )
plt.ylabel("PSNR")
## plot
y_psnr=[]
psnr_line, = ax_psnr.plot([0 for x in range(0,FRAME_NUM)], color='red')

############################### #### #####
###############################  BS  #####
ax_bs = fig.add_subplot(212)
plt.sca(ax_bs)
## plt.plot(x, y2[0:300], label='BS', color='blue')
# 设置sub1 两个坐标轴的范围
plt.xlim(0,FRAME_NUM)
plt.ylim(0,1024*300)
plt.grid() #开启网格#
# 主刻度
ax_bs.xaxis.set_major_locator( MultipleLocator(30) )
ax_bs.yaxis.set_major_locator( MultipleLocator(1024*30) )
plt.ylabel("BS")
## plot
y_bs=[]
bs_line, = ax_bs.plot([0 for x in range(0,FRAME_NUM)])


############################### update data ####
def init():
    global y_psnr
    global y_bs    
    y_psnr=[0 for x in range(0, FRAME_NUM)]
    y_bs=[0 for x in range(0, FRAME_NUM)]
    return y_psnr, y_bs

def update(i):
    psnr_line.set_data(x_plt, y_psnr)
    bs_line.set_data(x_plt, y_bs)
    return psnr_line, bs_line,


#动态画图
ani = animation.FuncAnimation(fig, update,
                              init_func=init,
                              interval=16)


#f=open(r'test_psnr.264','rb')
f=open(sys.argv[1], 'rb')
bs=[0 for x in range(0, 28)]
def data_gen():
    while 1:
        byte=f.read(1)
        if byte == "":
            print 'file over'
            sleep(2)
            break
        else:
            hexstr="%s" %byte.encode('hex')
            data=int(hexstr, 16)
            bs.append(data)
            del bs[0]

            if (bs[1]==0) and (bs[2]==0) and (bs[3]==0) and (bs[4]==1) and (bs[5]==127):
                y=bs[6]*256+bs[7]
                x=bs[9]*256+bs[10]
                mse=bs[13]*256*256*256*256+bs[15]*256*256*256+bs[16]*256*256+bs[18]*256+bs[19]
                bits=bs[21]*256*256*256+bs[22]*256*256+bs[24]*256+bs[25]
                psnr=round(10.0*math.log(255.0*255*y*x/mse)/math.log(10.0), 2)

                y_psnr.insert(0, psnr)
                y_bs.insert(0, bits)
                del y_psnr[FRAME_NUM:]
                del y_bs[FRAME_NUM:]
    
                print "Y=%d, X=%d, MSE=%d, PSNR=%0.2f, BITS=%d" %(y,x,mse,psnr,bits)
        


plist=[]
update_proc=threading.Thread(target=data_gen)
plist.append(update_proc)
ani_proc=threading.Thread(target=ani)
plist.append(ani_proc)

if __name__ == '__main__':
    for proc in plist:
        proc.setDaemon(True)
        proc.start()
    proc.join


plt.show()
raw_input()

