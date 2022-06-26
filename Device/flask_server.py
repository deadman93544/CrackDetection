from flask import Flask, request, send_from_directory
import logging
from CrackDetection import CrackDetection

logging.basicConfig(level='INFO')
log = logging.getLogger('FLASK')

app = Flask(__name__)

dir = "C:\\Users\\Prabhat Ranjan\\Desktop\\gphoto\\"

crack_detection = CrackDetection.get_instance()


@app.route('/crack', methods=['POST'])
def fetch_capture_image():
    request_files = request.files
    log.info(request_files)
    return {"Success": True}
