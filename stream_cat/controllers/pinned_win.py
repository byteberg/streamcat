"""
===============================================================================
Copyright (c) 2024 Stream.Cat
Website: https://stream.cat
===============================================================================
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('GdkX11', '4.0')
from gi.repository import Gtk, Gdk, Adw, GdkX11
from stream_cat import configs, ui, models, utils
import uuid, os, json, math, subprocess


class PinnedWin:
    def __init__(self, app):
        self.app = app

        # Timer win
        hb = Gtk.HeaderBar()
        t = Gtk.Label()
        t.add_css_class("pinned-win-header-bar-label")
        hb.set_title_widget(t)
        hb.add_css_class("pinned-win-header-bar")

        self.win = Gtk.Window()
        self.win.set_titlebar(hb)
        self.win.set_resizable(False)
        self.win.set_default_size(200, 120)

        # def on_timer_win_close(win, switch):
        #     win.hide()
        #     # print("closed")
        #     # return True
        #
        # self.win.connect("close-request", on_timer_win_close, switch)
        #
        # timer_label = Gtk.Label()
        # timer_label.add_css_class("timer-win-label")
        # timer_label.set_text("00:00:00")
        #
        # c_timer.add_label(timer_label)
        #
        # self.win.set_child(timer_label)
        #
        # switch.connect("state-set", on_switch_activated, self.win)

    def show(self):
        def set_always_on_top(win):
            xid = GdkX11.X11Surface.get_xid(win.get_surface())
            subprocess.run(['wmctrl', '-i', '-r', str(xid), '-b', 'add,above'])

        self.win.present()
        set_always_on_top(self.win)

    def hide(self):
        self.win.hide()
