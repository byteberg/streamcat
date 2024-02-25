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
from stream_cat import ui


class Settings:
    def __init__(self, app):
        self.app = app

    def show_window(self):
        if self.app.settings_win is None or not self.app.settings_win.is_visible():
            self.app.settings_win = Gtk.Window(title="Settings")
            self.app.settings_win.set_default_size(400, 400)
            ui.window_header(self.app.ASSETS_PATH, self.app.settings_win)

        self.app.settings_win.present()
