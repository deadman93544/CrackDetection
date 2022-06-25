from Camera import Camera
from CrackDetection import CrackDetection

camera = Camera.get_instance()
crack_detection = CrackDetection.get_instance()
file = camera.run()
print(file)
crack_detection.detect_function(file)
