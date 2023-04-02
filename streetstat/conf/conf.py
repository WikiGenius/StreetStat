# Author: Muhammed Elyamani
# Date: 03/02/2023
# GitHub: https://github.com/WikiGenius

import os
from kivy import platform

###########################<PLATFORM SETTINGS>###############################

# if platform == "android":
#     PLATFORM_ANDROID = True
# else:
#     PLATFORM_ANDROID = False
PLATFORM_ANDROID = True    
if PLATFORM_ANDROID:
    # model_tflite_path = './assets/weights/yolov6n_model.tflite'
    model_tflite_path = './assets/weights/yolov8n_float16.tflite'
    YOLOV8 = 'v8' in model_tflite_path

    print(f"Is the model existed: {os.path.isfile(model_tflite_path)}")

    
###########################<GLOBAL SETTINGS>###############################
THREAD = False
DEBUG=True
BAR_OPACITY = 0.8
MAX_FRAMES = 6
SKIP_FRAMES = 5