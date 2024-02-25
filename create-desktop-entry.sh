#!/bin/bash

EXECUTABLE_PATH=$PWD
ICON_PATH=$PWD

DESKTOP_ENTRY="[Desktop Entry]
Version=0.0.1-alpha
Type=Application
Name=Stream.Cat
GenericName=Stream.Cat - Streaming Tools
Comment=Video streams viewer, manipulation, ...
Icon=${ICON_PATH}/StreamCat.svg
Exec=${EXECUTABLE_PATH}/StreamCat
Terminal=false
Categories=Qt;AudioVideo;Video;Viewer;
Keywords=cctv;viewer;live streaming;streaming tools;"

DESKTOP_FILE="$HOME/.local/share/applications/StreamCat.desktop"
echo "$DESKTOP_ENTRY" > "$DESKTOP_FILE"
chmod +x "$DESKTOP_FILE"

echo "Desktop entry created at: $DESKTOP_FILE"

read -p "Create application shortcut on the desktop? (y/n): " choice
case "$choice" in
  y|Y )
    # Copy the .desktop file to the desktop directory
    cp "$DESKTOP_FILE" ~/Desktop/
    gio set ~/Desktop/StreamCat.desktop metadata::trusted true
    echo "Desktop shortcut created at: ~/Desktop/StreamCat.desktop";;
  n|N )
    echo "Desktop shortcut not created.";;
  * )
    echo "Invalid choice. Desktop shortcut not created.";;
esac