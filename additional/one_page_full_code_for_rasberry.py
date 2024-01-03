from gpiozero import MotionSensor
from picamera2 import Picamera2, Preview
import time
from datetime import datetime
import keyboard
import threading

import firebase_admin
from firebase_admin import credentials, storage, db

import numpy as np
import tensorflow as tf
from PIL import Image

cred = credentials.Certificate('path/to/your/firabase/json/file')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'your-firebase-storage-url',
    'databaseURL': 'your-firebase-realtime-db-url'
})

bucket = storage.bucket()
db_ref = db.reference('/')

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")

model_path = 'your-model-path' #trained ai model path

interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

keep_listening = True

def classify_animal(image_path):
    image = Image.open(image_path).convert('L')
    image = image.resize((96, 96)) #adjust the input size

    
    input_data = np.expand_dims(np.array(image), axis=0) #Convert to FLOAT32 and normalize
    input_data = np.expand_dims(input_data, axis=-1)
    input_data = input_data.astype(np.float32) / 255.0 #convert to float32
    
    # if input_data.shape != input_details[0]['shape'][1:]:
        # raise ValueError(f"Input tensor shape mismatch. Expected {input_details[0]['shape'][1:]}, got {input_data.shape} .")
    
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    print("Raw Output Data", output_data) #to test
    
    class_index = np.argmax(output_data)
    
    return class_index


def capture_photo():
    try:
        picam2.configure(camera_config)
        picam2.start_preview(Preview.QTGL)
        picam2.start()
        time.sleep(1) #delay
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"photo_{now}.jpg"
        picam2.capture_file(filename)
        picam2.stop_preview()
        picam2.stop()
        print("Photo Captured!")
        
        # image = Image.open(filename).convert('RGB')
        # resized_image = image.resize((96, 96)) #adjust the input size
        # resized_image_path = '/home/tiny/Desktop/resized_image.jpg'
        
        # try:
            # resized_image.save(resized_image_path)
            # print(f"Resized image saved:{resized_image_path}")
        # except Exception as e:
            # print(f"Error saving resized image: {e}")
        
        #Upload image to firebase Storage
        blob = bucket.blob(filename)
        blob.upload_from_filename(filename)
        
        #Storage image name in Firebase Realtime Database
        #db_ref.child('images').push({'name': filename})
        
        #Classify animal
        class_index = classify_animal(filename)
        print(f"Animal Class Index: {class_index}")
        
        class_name = "class0" if class_index == 0 else "class1"

        db_ref.child('images').push({'name': filename, 'class': class_name})
        print("Photo Captured and Uploaded to Firebase successfully!")
    except Exception as e:
        print("Error capturing photo: ", e)
        
pir = MotionSensor(4)

def input_listener():
    global keep_listening
    last_capture = time.time()
    while keep_listening:
        pir.wait_for_motion()
        print("Motion Detected!")
        if time.time() - last_capture > 5:
            capture_photo()
            last_capture = time.time()
        time.sleep(1)
        # user_input = input("press 'p' to capture photo or 'e' to exit")
        # if user_input == 'p':
            # capture_photo()
        # elif user_input == 'e':
            # keep_listening = False
    

#thread
key_listener_thread = threading.Thread(target=input_listener, args=(), daemon=True)
key_listener_thread.start()

try:
    while key_listener_thread.is_alive():
        time.sleep(1)
except KeyboardInterrupt:
    keep_listening = False

key_listener_thread.join()
print("Program exited.")

