"""
===============================================================================
Copyright (c) 2024 Stream.Cat
Website: https://stream.cat
===============================================================================
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk, Gio
from stream_cat import configs, ui, models, controllers
import os

def add_sidebar_camera(app, camera):
    def open_form(btn, app, the_camera2):
        ui.camera_form_window(app, the_camera2)

    def create_btn(icon, icon_class, btn_class):
        # Icon
        svg = Gtk.Image.new_from_file(os.path.join(app.ASSETS_PATH, 'icons', icon))
        svg.set_property("width-request", 24)
        svg.set_property("height-request", 24)

        img_box = Gtk.Box(spacing=0)
        img_box.add_css_class(icon_class)
        img_box.append(svg)
        img_box.set_property("valign", "center")
        img_box.set_property("halign", "center")

        btn = Gtk.Button()
        btn.set_child(img_box)
        btn.add_css_class(btn_class)
        btn.set_cursor(Gdk.Cursor().new_from_name('pointer'))
        btn.set_property("width-request", 34)
        btn.set_property("height-request", 34)
        return btn

    item_box = Gtk.Box()
    item_box.set_hexpand(True)

    camera_btn = Gtk.Button()
    camera_btn.set_hexpand(True)
    camera_btn.set_cursor(Gdk.Cursor().new_from_name('pointer'))
    camera_btn.set_property("height-request", 34)
    label = Gtk.Label(label=camera.name)
    label.set_ellipsize(gi.repository.Pango.EllipsizeMode.END)
    label.set_halign(Gtk.Align.START)
    camera_btn.set_child(label)
    item_box.append(camera_btn)

    edit_btn = create_btn("pen.svg", "sidebar-camera-btn-icon", "sidebar-camera-btn")
    edit_btn.set_margin_start(3)
    edit_btn.connect('clicked', open_form, app, camera)
    item_box.append(edit_btn)

    c = controllers.CameraController(app)

    pin_btn = create_btn("pin.svg", "sidebar-camera-btn-icon", "sidebar-camera-btn")
    pin_btn.set_margin_start(3)
    pin_btn.connect('clicked', c.pin_camera, camera)
    item_box.append(pin_btn)

    delete_btn = create_btn("trash.svg", "sidebar-camera-btn-icon", "sidebar-camera-btn")
    delete_btn.set_margin_start(3)
    delete_btn.connect('clicked', c.remove_camera, camera)
    item_box.append(delete_btn)

    app.sidebar_cameras.append(item_box)


class Sidebar:
    def about(self):
        about = Gtk.Box()
        about.set_orientation(Gtk.Orientation.VERTICAL)
        about.add_css_class('sidebar-about')
        self.box.append(about)

        # Program name & version
        label = Gtk.Label(label="Stream.Cat v" + configs.APP_VERSION)
        about.append(label)

        # Program Link
        def open_link(button, link):
            Gio.AppInfo.launch_default_for_uri(link, None)

        link = Gtk.Button(label="https://stream.cat")
        link.add_css_class('link')
        link.set_margin_top(5)
        link.set_cursor(Gdk.Cursor().new_from_name('pointer'))
        link.connect("clicked", open_link, 'https://stream.cat')
        about.append(link)

        # todo Donate button to support project =)
        if configs.APP_IS_TOMORROW:
            link = Gtk.Button(label="Donate")
            link.add_css_class('donate-link')
            link.set_margin_top(5)
            link.set_cursor(Gdk.Cursor().new_from_name('pointer'))
            link.connect("clicked", open_link, 'https://stream.cat/donate')
            about.append(link)

    def floor(self):
        # todo floor chart
        floor = Gtk.Box()

    def joystick_ptz(self):
        # todo camera PTZ tool
        if configs.APP_IS_TOMORROW:
            ptz_grid = Gtk.Grid()
            ptz_grid.insert_row(3)
            ptz_grid.insert_column(3)
            ptz_grid.add_css_class('sidebar-ptz')
            self.box.append(ptz_grid)
            # center_layout.set_center_widget(ptz_grid)

            ptz_btn = Gtk.Button(label="←")
            ptz_btn.add_css_class('sidebar-ptz-btn')
            ptz_btn.set_cursor(Gdk.Cursor().new_from_name('pointer'))
            ptz_btn.set_property("width-request", 34)
            ptz_btn.set_property("height-request", 34)
            ptz_grid.attach(ptz_btn, 0, 1, 1, 1)

            ptz_btn = Gtk.Button(label="→")
            ptz_btn.add_css_class('sidebar-ptz-btn')
            ptz_btn.set_cursor(Gdk.Cursor().new_from_name('pointer'))
            ptz_btn.set_property("width-request", 34)
            ptz_btn.set_property("height-request", 34)
            ptz_grid.attach(ptz_btn, 2, 1, 1, 1)

            ptz_btn = Gtk.Button(label="↑")
            ptz_btn.add_css_class('sidebar-ptz-btn')
            ptz_btn.set_cursor(Gdk.Cursor().new_from_name('pointer'))
            ptz_btn.set_property("width-request", 34)
            ptz_btn.set_property("height-request", 34)
            ptz_grid.attach(ptz_btn, 1, 0, 1, 1)

            ptz_btn = Gtk.Button(label="↓")
            ptz_btn.add_css_class('sidebar-ptz-btn')
            ptz_btn.set_cursor(Gdk.Cursor().new_from_name('pointer'))
            ptz_btn.set_property("width-request", 34)
            ptz_btn.set_property("height-request", 34)
            ptz_grid.attach(ptz_btn, 1, 2, 1, 1)

    def cameras_and_grid(self):
        # Sidebar cameras
        self.sidebar_cameras = Gtk.Box(spacing=5)
        self.sidebar_cameras.add_css_class('sidebar-cameras')
        self.sidebar_cameras.set_orientation(Gtk.Orientation.VERTICAL)
        # self.sidebar.append(self.sidebar_cameras)

        sidebar_cameras_scroll = Gtk.ScrolledWindow()
        sidebar_cameras_scroll.set_vexpand(True)
        sidebar_cameras_scroll.set_child(self.sidebar_cameras)

        def on_tab_switch(notebook, page, page_num):
            print(f"Switched to page {page_num + 1}")

        notebook = Gtk.Notebook()

        # Cameras Tab
        page = Gtk.Box()
        page.set_orientation(Gtk.Orientation.VERTICAL)
        page_label = Gtk.Label()
        page_label.set_text('Cameras')
        notebook.append_page(page, page_label)

        # - camera add button
        camera_add_btn = Gtk.Button(label="Add camera")
        camera_add_btn.set_margin_top(10)
        camera_add_btn.set_margin_end(10)
        camera_add_btn.set_margin_bottom(10)
        camera_add_btn.set_margin_start(10)
        camera_add_btn.set_cursor(Gdk.Cursor().new_from_name('pointer'))
        camera_add_btn.set_property("height-request", 34)
        page.append(camera_add_btn)
        camera_add_btn.connect('clicked', lambda x: ui.camera_form_window(self.app, models.Camera("", "", "")))

        label = Gtk.Label(label="Cameras")
        label.set_halign(Gtk.Align.START)
        label.set_margin_top(0)
        label.set_margin_end(10)
        label.set_margin_bottom(10)
        label.set_margin_start(10)

        page.append(label)
        page.append(sidebar_cameras_scroll)

        # todo grid settings: merge, resize, combine, ...
        if configs.APP_IS_TOMORROW:
            # Grid Tab
            page = Gtk.Box()
            page.set_orientation(Gtk.Orientation.VERTICAL)

            label = Gtk.Label(label="Grid settings", halign=Gtk.Align.START, valign=Gtk.Align.END)
            label.add_css_class('coming-soon-h')
            label.set_halign(Gtk.Align.CENTER)
            page.append(label)

            label = Gtk.Label(label="Coming soon", halign=Gtk.Align.START, valign=Gtk.Align.END)
            label.add_css_class('coming-soon')
            label.set_halign(Gtk.Align.CENTER)
            page.append(label)

            page_label = Gtk.Label()
            page_label.set_text('Grid')
            notebook.append_page(page, page_label)

        notebook.set_show_border(False)
        notebook.connect("page-added", on_tab_switch)
        self.box.append(notebook)

    def __init__(self, app):
        self.app = app
        self.sidebar_cameras = Gtk.Box()

        self.box = Gtk.Box(spacing=5)
        self.box.add_css_class('sidebar')
        self.box.set_size_request(250, 0)
        self.box.set_orientation(Gtk.Orientation.VERTICAL)

        self.about()
        self.floor()
        self.joystick_ptz()
        self.cameras_and_grid()
