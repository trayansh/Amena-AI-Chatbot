#!/bin/bash
apt-get install portaudio19-dev python-all-dev
apt-get install ffmpeg
pip install -r r.txt
gradio main.py
