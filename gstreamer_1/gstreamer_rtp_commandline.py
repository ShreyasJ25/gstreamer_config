#this program intializes gstreamer to start a video stream and
#simultaneously saves the video on a rolling basis.
#The timing of each videostream saved can be changed

#This script is used for  rtp streaming

#It directly calls the terminal command to carry out its functioning

#The name of the file which are being stored,are
#timestamps of those files when they are being intialized

#the streamed video on reciever can be watched using  udprecieving protocol

#the udp recieving protocol
#  gst-launch-1.0 udpsrc address=127.0.0.1  port=5000 
#! application/x-rtp,media=video,encoding-name=H264,clock-rate=90000 !
# rtpjitterbuffer latency=300 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! autovideosink -v

import os
import time
import psutil
import threading
from datetime import datetime

def fun():
    time.sleep(30) #5 minutes
    print("killing")
    no='gst-launch-1.0'
    onlysender='gst-launch-1.0 -e'
    """
    #this is another way to kill the process
    for proc in psutil.process_iter():
        if proc.name() == no:
            cod=os.system('kill -9 {}'.format(proc.pid))
    """
    code = os.system("pkill -f {}".format(onlysender))
    time.sleep(0.01)
    
def func(n3):
    print("intialised")
    code ="gst-launch-1.0 -e  v4l2src device=/dev/video0 ! videoconvert ! video/x-raw, format=YUY2 , width=1280,height=720,framerate=30/1  ! videoconvert ! videorate ! omxh264enc ! tee name=t   t. ! queue  ! rtph264pay ! udpsink host=192.168.1.11 port=5000    t.  ! queue ! h264parse ! avimux ! filesink location = {}".format(n3)
    var1=os.system(code)
    time.sleep(0.01)
while True:
    now=datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    print('newfile')

    now=str(now)
    n1=str('.avi')
    n2='/home/pi/cctv/storage3/'
    n3=n2+now+n1
    t1= threading.Thread(target=func,args=(n3,))
    t2= threading.Thread(target=fun)
    t1.start()
    t2.start()

    t1.join()
    t2.join()
    time.sleep(0.01)

print("hello")

