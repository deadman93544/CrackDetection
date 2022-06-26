from flask import Flask, request
import os
import logging
from Camera import Camera
import requests

logging.basicConfig(level='INFO')
log = logging.getLogger("FLASK")

app = Flask(__name__)

# dir = "/home/gaurav/Desktop/gphoto/images/"


def send_captured_image(file):
    try:
        log.info('Sending Captured Image')
        url = 'http://192.168.1.38:5000/crack'

        req = requests.post(url, files={'cam': file})
        resp = req.json()
        log.info(resp)
    except Exception as e:
        log.warning(e)
