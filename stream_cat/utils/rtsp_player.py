"""
===============================================================================
Copyright (c) 2024 Stream.Cat
Website: https://stream.cat
===============================================================================
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gst', '1.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk, Gst, Gdk, GdkPixbuf, GLib

# Initialize GStreamer
Gst.init(None)


class RTSPPlayer:
    def __init__(self, camera, picture):
        if camera.rtsp_url == "":
            return

        if picture is None:
            return

        self.picture = picture

        self.player = self.build_pipeline(camera)

        sink = self.player.get_by_name("mysink")
        if sink is None:
            print("Unable to find the sink element")
            # exit(1)
            return
        sink.connect("new-sample", self.on_new_sample)

        # Get error messages (todo in tomorrow save to logs or sent to stream.cat server)
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

        # Play stream
        self.player.set_state(Gst.State.PLAYING)

        # player_state = self.player.get_state(Gst.SECOND)

    def build_pipeline(self, camera):
        # Gst.parse_launch()
        # "rtspsrc location=rtsp://192.168.1.205:554/live/ch00_0 protocols=tcp ! "
        # "rtph264depay ! h264parse ! queue ! openh264dec ! videoconvert ! videoscale ! appsink name=mysink emit-signals=True caps=video/x-raw,format=(string)RGB"

        pipeline = Gst.Pipeline()

        # Create elements
        source = Gst.ElementFactory.make("rtspsrc", "source")
        source.set_property("location", camera.rtsp_url)
        source.set_property("protocols", "tcp")

        depay = Gst.ElementFactory.make("rtph264depay", "depay")
        parse = Gst.ElementFactory.make("h264parse", "parse")
        queue = Gst.ElementFactory.make("queue", "queue")
        decoder = Gst.ElementFactory.make("openh264dec", "decoder")
        converter = Gst.ElementFactory.make("videoconvert", "converter")
        scaler = Gst.ElementFactory.make("videoscale", "scaler")

        sink = Gst.ElementFactory.make("appsink", "mysink")
        sink.set_property("emit-signals", True)
        caps = Gst.caps_from_string("video/x-raw,format=(string)RGB")
        sink.set_property("caps", caps)

        if not pipeline or not source or not depay or not parse or not queue or not decoder or not converter or not scaler or not sink:
            print("Not all elements could be created.")
            exit(-1)

        # Add elements to the pipeline
        elements = [source, depay, parse, queue, decoder, converter, scaler, sink]
        for elem in elements:
            pipeline.add(elem)

        # Link elements together
        # Note: rtspsrc will be linked to its next element dynamically because its pads are created at runtime
        def link_elements(src, sink):
            src.link(sink)

        source.connect("pad-added", lambda src, pad: pad.link(depay.get_static_pad("sink")))
        link_elements(depay, parse)
        link_elements(parse, queue)
        link_elements(queue, decoder)
        link_elements(decoder, converter)
        link_elements(converter, scaler)
        link_elements(scaler, sink)

        return pipeline

    def on_new_sample(self, sink):
        # if camera picture deleted or updated stop stream
        if self.picture is None:
            # Stop stream
            self.player.set_state(Gst.State.PAUSED)
            return Gst.FlowReturn.OK

        sample = sink.emit("pull-sample")
        if sample:
            caps = sample.get_caps()
            structure = caps.get_structure(0)
            width = structure.get_value('width')
            height = structure.get_value('height')

            # Extract Gst.Buffer
            buffer = sample.get_buffer()
            success, map_info = buffer.map(Gst.MapFlags.READ)
            if not success:
                return Gst.FlowReturn.ERROR

            # OTHER
            data = map_info.data
            rowstride = map_info.size // height  # Calculate the rowstride
            has_alpha = False  # Assuming data does not have an alpha channel
            channels = 3 if not has_alpha else 4
            size = (width, height)
            pixbuf = GdkPixbuf.Pixbuf.new_from_data(data, GdkPixbuf.Colorspace.RGB, has_alpha, 8, width,
                                                    height, rowstride, None, None)

            buffer.unmap(map_info)

            # Update Gtk.Picture in the main thread
            GLib.idle_add(self.update_picture, pixbuf)

            return Gst.FlowReturn.OK

    def update_picture(self, pixbuf):
        self.picture.set_pixbuf(pixbuf)
        return GLib.SOURCE_REMOVE  # Only run once

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print("Error: %s" % err, debug)
            # self.player.set_state(Gst.State.NULL)
        elif t == Gst.MessageType.EOS:
            print("End of stream")
            # self.player.set_state(Gst.State.NULL)
