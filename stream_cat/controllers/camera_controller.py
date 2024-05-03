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
from stream_cat import configs, ui, models, utils
import uuid, os, json, math


class CameraController:
    def __init__(self, app):
        self.app = app
        self.cameras = []  # List to hold camera objects

    def on_alert(self, dialog, response_id):
        self.app.camera_form_win.set_sensitive(True)
        dialog.destroy()

    def alert(self, title, text):
        self.app.camera_form_win.set_sensitive(False)

        dialog = Gtk.MessageDialog(
            transient_for=self.app.camera_form_win,
            # flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=title,
            secondary_text=text
        )

        dialog.connect("response", self.on_alert)
        dialog.show()

    def load_cameras(self):
        data = self.get_data()

        # Empty cameras
        while self.app.sidebar_cameras.get_first_child():
            self.app.sidebar_cameras.remove(self.app.sidebar_cameras.get_first_child())

        # sidebar cameras
        for cam in data:
            the_camera = models.Camera(cam['uid'], cam['name'], cam['rtsp_url'])
            ui.add_sidebar_camera(self.app, the_camera)

        # Remove pages
        num_pages = self.app.cameras_notebook.get_n_pages()
        for _ in range(num_pages):
            self.app.cameras_notebook.remove_page(0)

        total_pages = math.ceil(len(data) / 4)
        cameras_spacing = 10
        cameras_grids = []
        for i in range(total_pages):
            cameras_grid = Gtk.Grid()
            cameras_grids.append(cameras_grid)
            cameras_grid.set_column_spacing(cameras_spacing)
            cameras_grid.set_row_spacing(cameras_spacing)
            cameras_grid.set_margin_top(cameras_spacing)
            cameras_grid.set_margin_end(cameras_spacing)
            cameras_grid.set_margin_bottom(cameras_spacing)
            cameras_grid.set_margin_start(cameras_spacing)
            cameras_grid.insert_row(2)
            cameras_grid.insert_column(2)
            cameras_grid.set_hexpand(True)
            page_label = Gtk.Label()
            page_label.set_text("Page " + str(i + 1))
            self.app.cameras_notebook.append_page(cameras_grid, page_label)

        camera_num = 0
        i, j = 0, 0
        previous_page, current_page = 0, 0
        for cam in data:
            camera_num += 1
            current_page = math.ceil(camera_num / 4)
            if current_page > previous_page:
                i, j = 0, 0

            if j == 2:
                i += 1
                j = 0

            the_camera = models.Camera(cam['uid'], cam['name'], cam['rtsp_url'])

            camera_box, picture = ui.camera_view(the_camera)

            cameras_grids[current_page - 1].attach(camera_box, j, i, 1, 1)

            j += 1
            previous_page = current_page

            # Camera streaming
            utils.RTSPPlayer(the_camera, picture)

    def discover_cameras(self):
        # Code to discover available cameras
        # For example, querying connected devices or IP addresses
        pass

    # Get cameras.json data
    def get_data(self):
        cameras_config_file = os.path.join(configs.APP_CONFIG_DIR, "cameras.json")
        if os.path.exists(cameras_config_file):
            with open(cameras_config_file, "r") as json_file:
                return json.load(json_file)

        return []

    def save_data(self, data):
        cameras_config_file = os.path.join(configs.APP_CONFIG_DIR, "cameras.json")
        with open(cameras_config_file, "w") as json_file:
            json.dump(data, json_file, indent=4)

    def save_camera(self, btn, camera_uid, name_entry, url_entry):
        camera_name = name_entry.get_text()
        if camera_name == "":
            self.alert("Something is empty", "Please fill camera name!")
            return

        camera_url = url_entry.get_text()
        if camera_url == "":
            self.alert("Something is empty", "Please fill camera url!")
            return

        is_new = False
        if camera_uid == "":
            is_new = True
            camera_uid = str(uuid.uuid4())
        the_cam = models.Camera(camera_uid, camera_name, camera_url)

        # Update data
        data = self.get_data()
        if is_new:
            # Append new camera data to the list
            data.append(the_cam.get_data())
        else:
            for i, dataItem in enumerate(data):
                if dataItem["uid"] == the_cam.uid:
                    data[i] = the_cam.get_data()
        self.save_data(data)

        # Close window
        if self.app.camera_form_win is not None:
            self.app.camera_form_win.close()

        self.load_cameras()

    def pin_camera(self, btn, the_cam):
        self.app.pinned_win.show()

        camera_box, picture = ui.camera_view(the_cam)
        self.app.pinned_win.win.set_child(camera_box)

        # cameras_grids[current_page - 1].attach(camera_box, j, i, 1, 1)

        # Camera streaming
        utils.RTSPPlayer(the_cam, picture)

        # def delete_confirm(dialog2, response_id):
        #     dialog2.destroy()
        #     if response_id == Gtk.ResponseType.YES:
        #         data = self.get_data()
        #         for i, dataItem in enumerate(data):
        #             if dataItem["uid"] == the_cam.uid:
        #                 data.pop(i)
        #         self.save_data(data)
        #         self.load_cameras()
        #
        # dialog = Gtk.MessageDialog(
        #     transient_for=self.app.camera_form_win,
        #     # flags=0,
        #     message_type=Gtk.MessageType.QUESTION,
        #     buttons=Gtk.ButtonsType.YES_NO,
        #     text="Really delete this camera?",
        # )
        #
        # dialog.set_transient_for(self.app)
        # dialog.set_modal(self.app)
        # dialog.connect("response", delete_confirm)
        # dialog.show()

    def remove_camera(self, btn, the_cam):
        def delete_confirm(dialog2, response_id):
            dialog2.destroy()
            if response_id == Gtk.ResponseType.YES:
                data = self.get_data()
                for i, dataItem in enumerate(data):
                    if dataItem["uid"] == the_cam.uid:
                        data.pop(i)
                self.save_data(data)
                self.load_cameras()

        dialog = Gtk.MessageDialog(
            transient_for=self.app.camera_form_win,
            # flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Really delete this camera?",
        )

        dialog.set_transient_for(self.app)
        dialog.set_modal(self.app)
        dialog.connect("response", delete_confirm)
        dialog.show()

    def start_capture(self, camera_name):
        # Code to start capturing images from a specific camera
        # For example, initializing camera capture
        pass

    def stop_capture(self, camera_name):
        # Code to stop capturing images from a specific camera
        # For example, releasing camera resources
        pass