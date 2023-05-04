#this is code is forged after multiple iterations of other scripts in gstreamer folder
#this script is inspired by implementaion in other script


#this script spawns an instance of gstreamer sending the data over rtmp protocol
#also this program  cuts the continious stream of data into parts of given duration for saving and uploads it to GCP bucket
#the files aree named from 0 to 24 which correspondsto 24 hours in a day


#this code is inspired by 'gstreamer_rtmp_commandline.py' and 'delete_upload.py'
#refer the above files for detailed expliantion

import sys
import signal
import os
import time
import psutil
import threading
from datetime import datetime
import fnmatch
import os
import cv2
from google.cloud import storage

dir_path = '/home/pi/cctv/storage3'
count = len(fnmatch.filter(os.listdir(dir_path), '*.avi')) #'*.*'
# Set the path to the service account key file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/pi/cctv/service_account_gcp.json'
# Create a Google Cloud Storage client
client = storage.Client()
# Set the name of the bucket you want to upload to
bucket_name = 'first_surveyaan_cctv'
# Get a reference to the bucket
bucket = client.bucket(bucket_name)

#print('File Count:', count)
number=0

code = os.system("pkill -f {}".format('gst-launch-1.0 -e'))#to end the process which has previously has not been closed

#interrupt handler function 
def handle_int(signal,frame):
    print("ctrl+c is pressed ending...")
    sys.exit()
    var=os.system("pkill -f {}".format('gst-launch-1.0 -e'))
      
#registering the signal handler
signal.signal(signal.SIGINT,handle_int)





def upload_delete():
    global number
    list_of_files = os.listdir(dir_path)
    full_path = [str(dir_path)+"/{0}".format(x) for x in list_of_files]

    if (len(list_of_files) > 1):

        
        oldest_file = min(full_path, key=os.path.getctime) #oldest file is localted
        print(oldest_file)
        
        # Set the path to the file you want to upload
        file_path = str(os.path.abspath(oldest_file))
        #renaming the file
        new_file_name = str(number)
        num=0
        with threading.Lock():
            number=number+1
            number=number%24
            num=(number-1)%24
        
        blob = bucket.blob(new_file_name)
        blob.upload_from_filename(file_path)
        
        #waiting for uploading to finish
        print('started to upload');
        t1=time.time()
        while not blob.exists():
            continue
        t2= time.time()-t1
        print('{} seconds ,uploaded {}'.format(t2,num))
        #deleting the uploaded video file
            
        os.remove(os.path.abspath(oldest_file))
        print('delete')
        list_of_files = os.listdir(dir_path)
        full_path = [str(dir_path)+"/{0}".format(x) for x in list_of_files]


def fun_kill_save():
    time.sleep(300) #30 minutes
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
    
def fun_stream(n3):
    print("intialised")
    code ="gst-launch-1.0 -e  v4l2src device=/dev/video0  ! video/x-raw , width=1280,height=720, framerate=30/1  ! videoconvert  ! omxh264enc ! tee name=t   t.  ! queue ! h264parse ! avimux ! filesink location = {}  t.  ! h264parse ! flvmux ! rtmpsink location='rtmp://34.93.137.134:8080/live/stream' sync=false ".format(n3)
    var1=os.system(code)
    time.sleep(0.01)
while True:
    
    print('rtmp')
    now=datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    print('newfile')

    now=str(now)
    n1=str('.avi')
    n2='/home/pi/cctv/storage3/'
    n3=n2+now+n1
    t1= threading.Thread(target=fun_stream,args=(n3,))
    t2= threading.Thread(target=fun_kill_save)
    t3=threading.Thread(target =upload_delete)
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()
    time.sleep(0.01)
    

print("hello")

