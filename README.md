# Stream.Cat v0.0.1-alpha - Free open source CCTV camera stream viewer

Welcome to Stream.Cat, version 0.0.1-alpha! This project is currently in its alpha stage, where we're laying the groundwork for an open-source CCTV camera stream viewer.

**Supported protocols:**

- RTSP

**Our roadmap**

- ~~Make first alpha release :)~~
- Brainstorm the roadmap

Visit our official website: https://stream.cat

**Installing All Necessary Libraries**

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install python3-gi
sudo apt install libgtk-4-dev libgdk-pixbuf2.0-dev libadwaita-1-dev
sudo apt install libgtk-4-media-gstreamer
```

**Installing All Necessary Python Packages**

```bash
pip install PyGObject
pip install platformdirs
```

For PyCharm users, we recommend installing PyGObject-stubs.

**Building the Application**

1. First install `pyinstaller`:

```bash
pip install pyinstaller
```

2. Let's build:

```bash
/bin/bash build.sh
```

3. If anything isn't working or if you have any ideas or questions, you can contact us through our website https://stream.cat or add an issue to our GitHub repository https://github.com/byteberg/streamcat/issues.


Enjoy using Stream.Cat!