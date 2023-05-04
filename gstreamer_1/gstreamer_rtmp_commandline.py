#RTMP protocl
# bespoke implemtation for live streaming on web

#this program intializes gstreamer to start a video stream to a tcp link and
#simultaneously saves the video on a rolling basis.
#The timing of each videostream saved can be changed

#This script is used for  rtmp streaming

#It directly calls the terminal command to carry out its functioning

#The name of the file which are being stored coresponds to the
#timestamps of those files when they were intialized

#the streamed video on reciever can be watched using  rtmprecieving protocol

#the rtmp recieving command
# gst-launch-1.0 rtmpsrc location="rtmp://192.168.1.11:8080/live/stream" ! flvdemux !
# h264parse ! avdec_h264 ! videoconvert ! autovideosink

#'live' here is application name (try remebering rtmp setup in  /etc/nginx/nginx.conf  in reciever) 

#fuser /dev/video*
#use the above command to see the pid of process using camera resource
#kill it using
# kill -9 <pid>


#or
#pkill -f gst-launch-1.0

import os
import time
import psutil
import threading
from datetime import datetime

def fun():
    time.sleep(30) #30 minutes
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
    code ="gst-launch-1.0 -e  v4l2src device=/dev/video0  ! video/x-raw , width=1280,height=720, framerate=30/1  ! videoconvert  ! omxh264enc ! tee name=t   t.  ! queue ! h264parse ! avimux ! filesink location = {}  t.  ! h264parse ! flvmux ! rtmpsink location='rtmp://192.168.1.11:8080/live/stream' sync=false ".format(n3)
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


