"""
===============================================================================
Copyright (c) 2024 Stream.Cat
Website: https://stream.cat
===============================================================================
"""


class Camera:
    def __init__(self, uid, name, rtsp_url):
        self.uid = uid
        self.name = name
        self.rtsp_url = rtsp_url
        self.is_active = False

    def get_data(self):
        return {"uid": self.uid, "name": self.name, "rtsp_url": self.rtsp_url}

    def activate(self):
        # Code to activate the camera
        self.is_active = True
        print(f"Camera '{self.name}' activated.")

    def deactivate(self):
        # Code to deactivate the camera
        self.is_active = False
        print(f"Camera '{self.name}' deactivated.")
