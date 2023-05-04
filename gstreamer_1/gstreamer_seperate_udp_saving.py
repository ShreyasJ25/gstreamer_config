#sharing data through gstreamer using udplink and saving the videofile using 2 pipelines
#Two seperate pipeline are used here for saving the videofile and streaming the video file

#Note : It wouldnt be prudent to use this program to fulfil our requirement as it consumes
#       lot of CPU and using two piplines having overlapping functionality is inefficient

#Glancing the below script would be helpful in understanding the python implementation of gstreamer


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
pipeline2 = Gst.Pipeline()

# Create GStreamer video source element
video_src = Gst.ElementFactory.make('appsrc', 'video_src')
video_src.set_property('caps', Gst.Caps.from_string('video/x-raw,format=BGR,width=1280,height=720,framerate=30/1'))
pipeline.add(video_src)

video_src2 = Gst.ElementFactory.make('appsrc', 'video_src')
video_src2.set_property('caps', Gst.Caps.from_string('video/x-raw,format=BGR,width=1280,height=720,framerate=30/1'))
pipeline2.add(video_src2)

# Create GStreamer video convert element
video_convert = Gst.ElementFactory.make('videoconvert', 'video_convert')
pipeline.add(video_convert)

video_convert2 = Gst.ElementFactory.make('videoconvert', 'video_convert')
pipeline2.add(video_convert2)




video_encode1 = Gst.ElementFactory.make('omxh264enc', 'video_encode1')
pipeline.add(video_encode1)

video_encode2 =Gst.ElementFactory.make('h264parse', 'video_encode2')
pipeline.add(video_encode2)

video_encode3 =Gst.ElementFactory.make('rtph264pay', 'video_encode3')
pipeline.add(video_encode3)

# Create GStreamer video sink element
#file which saves video
video_encode12 = Gst.ElementFactory.make('omxh264enc', 'video_encode1')
pipeline2.add(video_encode12)

video_encode22 =Gst.ElementFactory.make('h264parse', 'video_encode2')
pipeline2.add(video_encode22)

video_encode32=Gst.ElementFactory.make('rtph264pay', 'video_encode3')
pipeline2.add(video_encode32)



video_sink = Gst.ElementFactory.make('filesink', 'video_sink')
video_sink.set_property('location', '/home/pi/cctv/storage2/output3.h264')
pipeline.add(video_sink)

#file which transmits data over udp

video_sink2 = Gst.ElementFactory.make('udpsink', 'video_sink2')
video_sink2.set_property('host','127.0.0.1')
video_sink2.set_property('port',5000)
pipeline2.add(video_sink2)


# Link GStreamer elements
video_src.link(video_convert)
video_convert.link(video_encode1)
video_encode1.link(video_encode2)
video_encode2.link(video_encode3)
video_encode3.link(video_sink)#first link to local storage


video_src2.link(video_convert2)
video_convert2.link(video_encode12)
video_encode12.link(video_encode22)
video_encode22.link(video_encode32)
video_encode32.link(video_sink2)#first link to local storage


# Start GStreamer pipeline
pipeline.set_state(Gst.State.PLAYING)
pipeline2.set_state(Gst.State.PLAYING)


# Capture and process video frames
while True:
    ret, frame = cap.read()
    if not ret:
        break

    if (cv2.waitKey(40) == 27):
        break
    
     
    
    # Convert frame to GStreamer buffer and push to video source element
    data=np.ndarray.tobytes(frame)#
    buffer=Gst.Buffer.new_wrapped(data)#
    buffer.pts=buffer.dts=Gst.CLOCK_TIME_NONE#
    #buffer = Gst.Buffer.new_wrapped(frame.tobytes())
    video_src.emit('push-buffer',buffer)  #saving to the file
    video_src2.emit('push-buffer',buffer)
    
    cv2.imshow("feed",frame)

 
# Release cv2 video capture object
cv2.destroyAllWindows()
cap.release()
# Stop GStreamer pipeline
pipeline.set_state(Gst.State.NULL)
pipeline2.set_state(Gst.State.NULL)









