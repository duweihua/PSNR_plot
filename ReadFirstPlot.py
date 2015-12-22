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

#f=open(r'2.264','rb')
f=open(sys.argv[1], 'rb')

bs=[0 for x in range(0, 28)]
have_user_data=0
y_psnr=[]
y_bs=[]

fbits=[]
start_frame_cnt=0
bits_cnt=0

ff=f.read()
f.close

for d in ff:
    hexstr="%s" %d.encode('hex')
    data=int(hexstr, 16)
    bs.append(data)
    del bs[0]
    bits_cnt=bits_cnt+8
    
    if (bs[1]==0) and (bs[2]==0) and (bs[3]==0) and (bs[4]==1):
        if (bs[5]==65) or (bs[5]==101):
            if (start_frame_cnt>0):
                fbits.append(bits_cnt)
                print "Frame=%d, Bits=%d" %(start_frame_cnt-1,bits_cnt)
            start_frame_cnt=start_frame_cnt+1
            bits_cnt=0
        elif (bs[5]==127):
            have_user_data=1
            y=bs[6]*256+bs[7]
            x=bs[9]*256+bs[10]
            mse=bs[13]*256*256*256*256+bs[15]*256*256*256+bs[16]*256*256+bs[18]*256+bs[19]
            bits=bs[21]*256*256*256+bs[22]*256*256+bs[24]*256+bs[25]
            psnr=round(10.0*math.log(255.0*255*y*x/mse)/math.log(10.0), 2)

            y_psnr.append(psnr)
            y_bs.append(bits)
            print "Y=%d, X=%d, MSE=%d, PSNR=%0.2f, BITS=%d" %(y,x,mse,psnr,bits)
        

fig=plt.figure(figsize=(15,9))
# 设置图的底边距
plt.subplots_adjust(top=0.98)
plt.subplots_adjust(bottom=0.05)
plt.subplots_adjust(left=0.08)
plt.subplots_adjust(right=0.97)


if have_user_data==1:
    lens=len(y_bs)
else:
    lens=len(fbits)
x_plt=np.arange(0,lens,1)
############################### #### #####
############################### PSNR #####
ax_psnr = fig.add_subplot(211)
plt.sca(ax_psnr) #set active fig
## plt.plot(x, y1[0:300], label='PSNR', color='red') #描点
# 设置sub1 两个坐标轴的范围
plt.xlim(0,lens)
psnr_min=min(y_psnr)-0.1
psnr_max=max(y_psnr)+0.1
if have_user_data==1:
    plt.ylim(psnr_min, psnr_max)
else:
    plt.ylim(29,31)
plt.grid() #开启网格#
# 主刻度
ax_psnr.xaxis.set_major_locator(MultipleLocator(30))
ax_psnr.yaxis.set_major_locator(MultipleLocator((psnr_max-psnr_min)/5))
plt.ylabel("PSNR")
## plot
if have_user_data==1:
    ax_psnr.plot(x_plt, y_psnr, color='red')
else:
    ax_psnr.plot(x_plt, fbits, color='red')

############################### #### #####
###############################  BS  #####
ax_bs = fig.add_subplot(212)
plt.sca(ax_bs)
## plt.plot(x, y2[0:300], label='BS', color='blue')
# 设置sub1 两个坐标轴的范围
plt.xlim(0,lens)
bs_min=min(y_bs)
bs_max=max(y_bs)
if have_user_data==1:
    plt.ylim(bs_min, bs_max)
else:
    plt.ylim(min(fbits), max(fbits))
plt.grid() #开启网格#
# 主刻度
ax_bs.xaxis.set_major_locator(MultipleLocator(30))
ax_bs.yaxis.set_major_locator(MultipleLocator((bs_max-bs_min)/5))
plt.ylabel("BS")
## plot
if have_user_data==1:
    ax_bs.plot(x_plt, y_bs)
else:
    ax_bs.plot(x_plt, fbits)

############################### update data ####
plt.show()
raw_input()

