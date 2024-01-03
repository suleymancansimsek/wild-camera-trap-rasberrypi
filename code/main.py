# main.py
from gpiozero import MotionSensor
import time
import threading
from camera_module import capture_photo
from ai_module import classify_animal
from firebase_module import initialize_firebase, upload_image_to_firebase

keep_listening = True

def input_listener(picam2, camera_config, bucket, db_ref):
    global keep_listening
    last_capture = time.time()
    while keep_listening:
        # ... (same code as in your original input_listener function)
        if time.time() - last_capture > 5:
            filename = capture_photo(picam2, camera_config)
            if filename:
                upload_image_to_firebase(bucket, filename)
                class_index = classify_animal(filename)
                class_name = "suleyman" if class_index == 0 else "hand"
                db_ref.child('images').push({'name': filename, 'class': class_name})
                print("Photo Captured and Uploaded to Firebase successfully!")
                last_capture = time.time()
        time.sleep(1)

def main():
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
    
    bucket, db_ref = initialize_firebase()

    pir = MotionSensor(4)

    # thread
    key_listener_thread = threading.Thread(target=input_listener, args=(picam2, camera_config, bucket, db_ref), daemon=True)
    key_listener_thread.start()

    try:
        while key_listener_thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        keep_listening = False

    key_listener_thread.join()
    print("Program exited.")

if __name__ == "__main__":
    main()
