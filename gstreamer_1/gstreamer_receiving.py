"""
udpreceving:
gst-launch-1.0 udpsrc address=192.168.1.11  port=8080! application/x-rtp,media=video,encoding-name=H264,clock-rate=90000! rtpjitterbuffer latency=300 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! autovideosink -v
"""

"""
gst-launch-1.0 udpsrc address=192.168.1.11 port=8080 ! application/x-rtp,media=video,encoding-name=H264,clock-rate=90000 ! rtpjitterbuffer latency=300 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! autovideosink -v

"""

"""
#for rtmp 
gst-launch-1.0 rtmpsrc location="rtmp://192.168.1.11:8080/live/stream" ! flvdemux ! h264parse ! avdec_h264 ! videoconvert ! autovideosink

"""

# this script  is implemetation of above command in detailed way using Gst
#this is , in mathematical terms ,is inverse of  'gstreamer_sending.py'
#'gstremaer_sending.py' sends the data and this script recieves the data


#1
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst , GLib

#GObject.threads_init()
Gst.init(None)

pipeline = Gst.Pipeline()

# Create udpsrc element to receive video
udpsrc = Gst.ElementFactory.make('udpsrc', 'udp-source')
udpsrc.set_property('address', '192.168.1.11')  # set the IP address to receive from
udpsrc.set_property('port', 8080)  # set the port to receive on


udpsrc.set_property('caps', Gst.Caps.from_string('application/x-rtp,media=video,encoding-name=H264,clock-rate=90000'))
# create a buffer
buff =Gst.ElementFactory.make('rtpjitterbuffer','buff')
buff.set_property('latency',300)


# Create RTP depayloader element
rtpdepay = Gst.ElementFactory.make('rtph264depay', 'rtpdepay')

parse =Gst.ElementFactory.make('h264parse','parse')

# Create avdec decoder element
dec = Gst.ElementFactory.make('avdec_h264','dec')


# Create videoconvert element to convert format to RGB
videoconvert = Gst.ElementFactory.make('videoconvert', 'videoconvert')

# Create autovideosink element to display video
sink = Gst.ElementFactory.make('autovideosink', 'sink')

# Add all elements to the pipeline
pipeline.add(udpsrc)
pipeline.add(buff)
pipeline.add(rtpdepay)
pipeline.add(parse)
pipeline.add(dec)
pipeline.add(videoconvert)
pipeline.add(sink)

# Link the elements
udpsrc.link(buff)
buff.link(rtpdepay)
rtpdepay.link(parse)
parse.link(dec)
dec.link(videoconvert)
videoconvert.link(sink)

# Start the pipeline
pipeline.set_state(Gst.State.PLAYING)

# Run the main loop to display video
loop = GLib.MainLoop()
try:
    loop.run()
except KeyboardInterrupt:
    pass

# Stop the pipeline
pipeline.set_state(Gst.State.NULL)



"""
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

# Initialize GStreamer
Gst.init(None)

# Define the GStreamer pipeline
pipeline_description = 'udpsrc address=192.168.1.11 port=8080! application/x-rtp,media=video,encoding-name=H264,clock-rate=90000! rtpjitterbuffer latency=300 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! autovideosink'
pipeline = Gst.parse_launch(pipeline_description)

# Start the pipeline
pipeline.set_state(Gst.State.PLAYING)

# Create a GMainLoop to run the pipeline
loop = GLib.MainLoop()
try:
    loop.run()
except KeyboardInterrupt:
    pass

# Stop the pipeline and clean up
pipeline.set_state(Gst.State.NULL)
"""
