"""
===============================================================================
Copyright (c) 2024 Stream.Cat
Website: https://stream.cat
===============================================================================
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk
import os

def init_style(assets_path):
    css_provider = Gtk.CssProvider()
    css_provider.load_from_path(os.path.join(assets_path, 'style.css'))
    context = Gtk.StyleContext
    screen = Gdk.Display.get_default()
    context.add_provider_for_display(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
