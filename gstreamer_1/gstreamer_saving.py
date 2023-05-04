#two instance of the same video is being saved here
#cv2 video writer saves the video as files of given duration and name of file would be its corresponding timestamp
#The gstreamer saves the video as one single file


#saving data through gstreamer and vidowriter of cv2
#video writer saves the video in avi format
#gstreamer encodes the video and saves in avi format
#cv2 uses video_writer functionality to save the same video but through its inbuilt encoding technique



import time
import cv2
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import time
import os
from datetime import datetime
import threading
import numpy as np

# Create cv2 video capture object
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
#not setting the capsize right will lead to erroneous result



# Initialize GStreamer
Gst.init(None)

# Create GStreamer pipeline
pipeline = Gst.Pipeline()

# Create GStreamer video source element
video_src = Gst.ElementFactory.make('appsrc', 'video_src')
video_src.set_property('caps', Gst.Caps.from_string('video/x-raw,format=BGR,width=1280,height=720,framerate=30/1'))
pipeline.add(video_src)

# Create GStreamer video convert element
video_convert = Gst.ElementFactory.make('videoconvert', 'video_convert')
pipeline.add(video_convert)
"""
# Create GStreamer video encode element      
#video_encode = Gst.ElementFactory.make('x264enc', 'video_encode')
#pipeline.add(video_encode)

"""

video_encode1 = Gst.ElementFactory.make('omxh264enc', 'video_encode1')
pipeline.add(video_encode1)

video_encode2 =Gst.ElementFactory.make('h264parse', 'video_encode2')
pipeline.add(video_encode2)

"""
video_encode3 =Gst.ElementFactory.make('rtph264pay', 'video_encode3')
pipeline.add(video_encode3)
"""
#mux
mux =Gst.ElementFactory.make('avimux','mux')
pipeline.add(mux)


# Create GStreamer video sink element
video_sink = Gst.ElementFactory.make('filesink', 'video_sink')
video_sink.set_property('location', '/home/pi/cctv/storage/output.avi')
pipeline.add(video_sink)

"""
video_sink2 = Gst.ElementFactory.make('udpsink', 'video_sink')
video_sink2.set_property('host','127.0.0.1')
video_sink2.set_property('port',5000)

pipeline.add(video_sink2)
"""

# Link GStreamer elements
video_src.link(video_convert)
#video_convert.link(video_encode)
video_convert.link(video_encode1)
video_encode1.link(video_encode2)
video_encode2.link(mux)
mux.link(video_sink)
#video_encode3.link(video_sink)


# Start GStreamer pipeline
pipeline.set_state(Gst.State.PLAYING)

dur=10
now=datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
print(now)
now=str(now)
n1=str('.avi')
n2='/home/pi/cctv/storage/'
n3=n2+now+n1
t1=time.time()
t2=time.time()+ dur
fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
out = cv2.VideoWriter(n3, fourcc, 5.0, (1280,720))


def video_save(frame,out):
    out.write(frame)


# Capture and process video frames
while True:
    ret, frame = cap.read()
    if not ret:
        break
    if (cv2.waitKey(40) == 27):
        break
    if  (time.time() >t2):
        
        out.release()
        now=datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        print(now)
        now=str(now)
        n1=str('.avi')
        n2='/home/pi/cctv/storage/'
        n3=n2+now+n1
        t1=time.time()
        t2=time.time()+ dur
        out = cv2.VideoWriter(n3, fourcc, 5.0, (1280,720))

    T2=threading.Thread(target=video_save,args=(frame,out,))
    T2.setDaemon(True)
    T2.start()
    T2.join()
    
    # Convert frame to GStreamer buffer and push to video source element
    """
    buffer = Gst.Buffer.new_wrapped(frame.tobytes())
    video_src.emit('push-buffer', buffer)
    cv2.imshow("feed",frame)
    """
    data=np.ndarray.tobytes(frame)#
    buffer=Gst.Buffer.new_wrapped(data)#
    buffer.pts=buffer.dts=Gst.CLOCK_TIME_NONE#
    video_src.emit('push-buffer',buffer)
    cv2.imshow("feed",frame)
    
    
# Release cv2 video capture object
out.release()
cv2.destroyAllWindows()
cap.release()


# Stop GStreamer pipeline
pipeline.set_state(Gst.State.NULL)







