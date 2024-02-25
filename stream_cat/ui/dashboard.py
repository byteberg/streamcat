"""
===============================================================================
Copyright (c) 2024 Stream.Cat
Website: https://stream.cat
===============================================================================
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk, Adw


class Dashboard:
    def __init__(self):
        # Cameras
        self.box = Gtk.Box()
        self.box.set_hexpand(True)
        self.box.set_vexpand(True)

        self.cameras_notebook = Gtk.Notebook()
        self.cameras_notebook.set_hexpand(True)
        self.cameras_notebook.set_vexpand(True)
        self.cameras_notebook.set_show_border(False)

        self.box.append(self.cameras_notebook)
