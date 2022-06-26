from flask import Flask, request, send_from_directory
import logging
from CrackDetection import CrackDetection
import time
from threading import Thread

logging.basicConfig(level='INFO')
log = logging.getLogger('FLASK')

app = Flask(__name__)

dir = "C:\\Users\\Prabhat Ranjan\\Desktop\\gphoto\\"

crack_detection = CrackDetection.get_instance()


@app.route('/crack', methods=['POST'])
def fetch_capture_image():
    request_files = request.files
    log.info(request_files)

    # crack_detection.detect_function(request_files['cam'])
    return {"Success": True}


#
# while True:
#     time.sleep(20)
t1 = Thread(target=lambda: app.run(host='0.0.0.0', debug=False, threaded=True, use_reloader=False))
t1.start()
