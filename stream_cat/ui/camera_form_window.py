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
from stream_cat import ui, controllers

def camera_form_window(app, camera):
    # app.set_sensitive(False)

    if app.camera_form_win is None or not app.camera_form_win.is_visible():
        # Header
        app.camera_form_win = Gtk.Window(title=("Add Camera" if camera.uid == "" else "Update Camera"))
        app.camera_form_win.set_default_size(400, -1)
        ui.window_header(app.ASSETS_PATH, app.camera_form_win)

        app.camera_form_win.set_transient_for(app)
        app.camera_form_win.set_modal(app)

    # Form grid
    grid = Gtk.Grid(column_homogeneous=True, column_spacing=10, row_spacing=10)
    grid.add_css_class("camera-add-form")
    app.camera_form_win.set_child(grid)

    # Name
    name_label = Gtk.Label(label="Camera Name:")
    name_label.set_halign(Gtk.Align.END)
    name_entry = Gtk.Entry()
    name_entry.set_text(camera.name)
    name_entry.set_hexpand(True)
    grid.attach(name_label, 0, 0, 1, 1)
    grid.attach_next_to(name_entry, name_label, Gtk.PositionType.RIGHT, 1, 1)

    # RTSP Link
    url_label = Gtk.Label(label="RTSP Link:")
    url_label.set_halign(Gtk.Align.END)
    url_entry = Gtk.Entry()
    url_entry.set_text(camera.rtsp_url)
    url_entry.set_hexpand(True)
    grid.attach(url_label, 0, 1, 1, 1)
    grid.attach_next_to(url_entry, url_label, Gtk.PositionType.RIGHT, 1, 1)

    # Submit button
    btn = Gtk.Button(label="Save Camera")
    btn.set_cursor(Gdk.Cursor().new_from_name('pointer'))

    cam = controllers.CameraController(app)
    btn.connect("clicked", cam.save_camera, camera.uid, name_entry, url_entry)

    grid.attach(btn, 0, 2, 2, 1)

    app.camera_form_win.present()
