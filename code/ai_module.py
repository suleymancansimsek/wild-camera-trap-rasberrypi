# image_utils.py
import numpy as np
import tensorflow as tf
from PIL import Image

model_path = 'ai/vww_96_grayscale_quantized.tflite' #this is important : train your ai and include in project if you want

interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


def classify_animal(image_path):
    image = Image.open(image_path).convert('L')
    image = image.resize((96, 96)) #adjust the input size

    
    input_data = np.expand_dims(np.array(image), axis=0)
    input_data = np.expand_dims(input_data, axis=-1)
    input_data = input_data.astype(np.float32) / 255.0 #convert to float32 and normalize
    
    # if input_data.shape != input_details[0]['shape'][1:]:
        # raise ValueError(f"Input tensor shape mismatch. Expected {input_details[0]['shape'][1:]}, got {input_data.shape} .")
    
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    print("Raw Output Data", output_data) #to see the result values
    
    class_index = np.argmax(output_data)
    
    return class_index