# camera_module.py
from picamera2 import Picamera2, Preview
import time
from datetime import datetime

def capture_photo(picam2, camera_config):
    try:
        picam2.configure(camera_config)
        picam2.start_preview(Preview.QTGL)
        picam2.start()
        time.sleep(1)  # delay
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"photo_{now}.jpg"
        picam2.capture_file(filename)
        picam2.stop_preview()
        picam2.stop()
        print("Photo Captured!")
        return filename
    except Exception as e:
        print("Error capturing photo: ", e)
        return None
