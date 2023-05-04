#sharing data through gstreamer using udplink
# The image here is being captured by cv2 which are encoded and sent using gstreamer

#The terminal command for this implementation of gstreamer is
#gst-launch-1.0 -e -v v4l2src device=/dev/video0 do-timestamp=1 
# ! video/x-raw, width=352, height=288, framerate=25/1 ! videoconvert ! omxh264enc  
#! h264parse ! rtph264pay ! udpsink host=127.0.0.1  port=5000 -ev

#The video stream can be viewed at the reciever using the following terminal command
#  gst-launch-1.0 udpsrc address=127.0.0.1  port=5000 
#! application/x-rtp,media=video,encoding-name=H264,clock-rate=90000 !
# rtpjitterbuffer latency=300 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! autovideosink -v



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

video_encode3 =Gst.ElementFactory.make('rtph264pay', 'video_encode3')
pipeline.add(video_encode3)

# Create GStreamer video sink element udp

video_sink2 = Gst.ElementFactory.make('udpsink', 'video_sink')
video_sink2.set_property('host','127.0.0.1')
video_sink2.set_property('port',5000)
pipeline.add(video_sink2)


# Link GStreamer elements
video_src.link(video_convert)
#video_convert.link(video_encode)
video_convert.link(video_encode1)
video_encode1.link(video_encode2)
video_encode2.link(video_encode3)
video_encode3.link(video_sink2)


# Start GStreamer pipeline
pipeline.set_state(Gst.State.PLAYING)

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
    video_src.emit('push-buffer',buffer)
    cv2.imshow("feed",frame)
    
    
# Release cv2 video capture object

cv2.destroyAllWindows()
cap.release()

# Stop GStreamer pipeline
pipeline.set_state(Gst.State.NULL)








