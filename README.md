# Camera Trap Project using RasberryPi



This is a repository for Camera Trap Project using RasberryPi

[VIDEO TUTORIAL (Soon)](https://www.youtube.com/@suleymancansimsek)

Key Features:
- 🍇 Usage of RasberryPi 4
- 🚀 Usage of Motion Detection Sensor (PIR)
- 📷 Usage of PiCamera
- 🐍 Working on Python projects
- 🧑‍💻 Basic Linux commends to install packages
- 📱 How to train AI in simpler way
- 🧠 Usage of AI on IOT project
- 🔓 Firebase storage and real-time database
- 📝 Fully IOT project 


### Prerequisites

- **Raspberry Pi 4** 
   ![Raspberry Pi 4](https://assets.raspberrypi.com/static/raspberry-pi-4-labelled@2x-1c8c2d74ade597b9c9c7e9e2fff16dd4.png)
- **Picamera**
   ![Picamera](https://image.robotistan.com/raspberry-pi-camera-modul-camera-modul-for-raspberry-pi-12935-16-O.jpg)
- **Motion Sensor (PIR)**
   ![Motion Sensor (PIR)](https://www.robotistan.com/hc-sr501-ayarlanabilir-ir-hareket-algilama-sensoru-pir-29012-17-B.jpg)

### Cloning the repository

```shell
git clone https://github.com/suleymancansimsek/wild-camera-trap-rasberrypi.git
```

### Install packages

These packages can be difficult to install and you may receive errors while installing. You can report any problems

```shell
sudo apt-get install python3-gpiozero python3-picamera2 python3-time python3-datetime python3-keyboard python3-threading python3-firebase python3-numpy python3-tensorflow python3-pil
```

### Setup config.py file


```py
# config.py
firebase_config = {
    'credential_path': '/path/to/your/credential.json',
    'storage_bucket': 'your-firebase-storage-bucket',
    'database_url': 'https://your-firebase-database-url.firebaseio.com',
}

```

### Train your AI model if you want

I used Teachable Machine to train my model   
[https://teachablemachine.withgoogle.com/train/tiny_image]

You can find related dataset from [kaggle](https://www.kaggle.com/code/min4tozaki/animal-classification/input)

### ⭐️ Give a star if you like it
