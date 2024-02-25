"""
===============================================================================
Copyright (c) 2024 Stream.Cat
Website: https://stream.cat
===============================================================================
"""

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
import os

def window_header(assets_path, window):
    # Window header (https://docs.gtk.org/gtk4/class.HeaderBar.html)
    header_bar = Gtk.HeaderBar()
    header_bar.set_show_title_buttons(True)

    # Add logo icon to header
    logo_image = Gtk.Image.new_from_file(os.path.join(assets_path, 'icon.svg'))
    logo_image.set_vexpand(True)
    logo_image.set_property("height-request", 35)
    logo_image.set_property("width-request", 35)

    logo_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    logo_box.append(logo_image)
    logo_box.set_property("height-request", 40)
    logo_box.set_property("width-request", 45)
    logo_box.add_css_class('headerbar-logo')

    header_bar.pack_start(logo_box)
    window.set_titlebar(header_bar)