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
from stream_cat import ui, configs, controllers
import sys, os

class StreamCatApp(Gtk.ApplicationWindow):
    def init_ui(self):
        # CSS Styles
        ui.init_style(self.ASSETS_PATH)

        # Window
        self.set_title(configs.APP_TITLE)
        self.set_default_size(1000, 650)

        # Header
        ui.window_header(self.ASSETS_PATH, self)

        # Create a grid
        grid = Gtk.Grid()
        grid.insert_column(2)
        grid.set_hexpand(True)
        grid.set_vexpand(True)
        # self.set_child(grid)

        # Menu
        menu = ui.menu(self)
        grid.attach(menu.box, 0, 0, 1, 1)

        # Dashboard
        dashboard = ui.Dashboard()
        self.cameras_notebook = dashboard.cameras_notebook
        grid.attach(dashboard.box, 1, 0, 1, 1)

        # Sidebar
        sidebar = ui.Sidebar(self)
        self.sidebar = sidebar.box
        self.sidebar_cameras = sidebar.sidebar_cameras
        # grid.attach(self.sidebar, 2, 0, 1, 1)

        # Paned
        paned = Gtk.Paned()
        paned.set_start_child(grid)
        paned.set_end_child(self.sidebar)

        paned.set_resize_start_child(True)
        paned.set_shrink_start_child(False)
        paned.set_resize_end_child(False)
        paned.set_shrink_end_child(False)

        self.set_child(paned)

        # def on_focus_in(window, event):
        #     print("Window focused")
        #
        # self.connect("activate-focus", on_focus_in)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ASSETS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")

        # windows
        self.settings_win = None
        self.camera_form_win = None
        self.sidebar = Gtk.Box()
        self.sidebar_cameras = Gtk.Box()
        self.cameras_notebook = Gtk.Notebook()

        # Pinned Window
        self.pinned_win = controllers.PinnedWin(self)

        # UI
        self.init_ui()

        # Load cameras
        camera_controller = controllers.CameraController(self)
        camera_controller.load_cameras()


class StreamCatAdw(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.win = None
        self.connect('activate', self.on_activate)

    def on_activate(self, main_app):
        self.win = StreamCatApp(application=main_app)
        self.win.present()


def run_stream_cat():
    # Create the config directory if it doesn't exist
    if not os.path.exists(configs.APP_CONFIG_DIR):
        os.makedirs(configs.APP_CONFIG_DIR)

    # Create and run a new application
    app = StreamCatAdw(application_id="com.StreamCat.GtkApplication")
    app.run(sys.argv)
    sys.exit(0)
