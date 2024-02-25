"""
===============================================================================
Copyright (c) 2024 Stream.Cat
Website: https://stream.cat
===============================================================================
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk

def camera_view(camera):
    camera_box = Gtk.Box()
    camera_box.add_css_class('camera-view')
    camera_box.set_hexpand(True)
    camera_box.set_vexpand(True)
    camera_box.set_orientation(Gtk.Orientation.VERTICAL)
    camera_box.set_size_request(300, 240)

    overlay = Gtk.Overlay()
    overlay.add_css_class('camera-view-overlay')
    overlay.set_hexpand(True)
    overlay.set_vexpand(True)
    camera_box.append(overlay)

    # Image
    picture = Gtk.Picture()
    picture.set_hexpand(True)
    picture.set_vexpand(True)
    picture.add_css_class('camera-view-img')
    overlay.add_overlay(picture)

    # Label
    label = Gtk.Label(label=camera.name, halign=Gtk.Align.START, valign=Gtk.Align.END)
    label.add_css_class('camera-view-name')
    label.set_hexpand(True)
    label.set_max_width_chars(30)
    label.set_ellipsize(gi.repository.Pango.EllipsizeMode.END)
    label.set_halign(Gtk.Align.START)
    overlay.add_overlay(label)

    overlay.set_child_visible(label)

    return camera_box, picture
