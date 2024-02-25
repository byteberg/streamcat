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
from stream_cat import configs
import os

class menu():
    def create_btn(self, icon):
        # Icon
        svg = Gtk.Image.new_from_file(os.path.join(self.app.ASSETS_PATH, 'icons', icon))
        svg.set_property("width-request", 24)
        svg.set_property("height-request", 24)

        img_box = Gtk.Box(spacing=0)
        img_box.add_css_class("menu-btn-icon")
        img_box.append(svg)
        img_box.set_property("valign", "center")
        img_box.set_property("halign", "center")

        btn = Gtk.Button()
        btn.set_child(img_box)
        btn.add_css_class("menu-btn")
        btn.set_cursor(Gdk.Cursor().new_from_name('pointer'))
        btn.set_property("width-request", 34)
        btn.set_property("height-request", 34)

        self.box.append(btn)

        return btn
    def __init__(self, appWindow):
        self.box = Gtk.Box(spacing=5)
        self.box.add_css_class('menu')
        self.box.set_orientation(Gtk.Orientation.VERTICAL)

        self.app = appWindow

        btn_home = self.create_btn("home.svg")
        btn_home.add_css_class('active')

        # todo menus: notifications, recording, languages
        if configs.APP_IS_TOMORROW:
            btn_menu = self.create_btn("menu.svg")
            btn_notifications = self.create_btn("drive-multidisk-symbolic.svg")
            btn_notifications = self.create_btn("bell.svg")
            btn_ = self.create_btn("3d-cube.svg")
            btn_lang = self.create_btn("language.svg")

        empty_box = Gtk.Box()
        empty_box.set_vexpand(True)
        self.box.append(empty_box)

        # todo settings
        if configs.APP_IS_TOMORROW:
            btn_settings = self.create_btn("cog.svg")
            # btn_settings.connect('clicked', lambda x: self.settings_window())

        btn_close = self.create_btn("times.svg")
        btn_close.connect('clicked', lambda x: appWindow.close())
