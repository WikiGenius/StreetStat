# Author: Muhammed Elyamani
# Date: 03/02/2023
# GitHub: https://github.com/WikiGenius

from threading import Thread
from utils import get_model, preprocess
import time
from conf import *
import numpy as np

class Detector:
    def __init__(self, model_tflite_path, use_cuda=False):        
        self.use_cuda = use_cuda
        self.interpreter, self.input_details, self.output_details = get_model(
            model_tflite_path)
        if YOLOV8:
            self.input_shape = self.input_details[0]['shape'][1:3]
        else:
            self.input_shape = self.input_details[0]['shape'][2:]
            
        self.output_data = []
        # Variable to control when model is stopped
        self.stopped = True
        self.detect_started = False
        self.thread_detect = False
        
    def start(self):
        # Start the thread that update_detection
        self.thread_detect = True
        Thread(target=self.update_detection, args=(), daemon=True).start()
        return self

    def stop(self):
        # Indicate that the camera and thread should be stopped
        self.stopped = True
        
    def update_detection(self):
        while True:
            if not self.stopped:
                self.detection_process()

                    
    def detection_process(self):

        transpose=False
        if not YOLOV8:
            transpose = True
        im, self.ratio, self.dwdh = preprocess(self.img, self.input_shape, transpose)
        
        # predict the model
        input = self.input_details[0]
        self.interpreter.set_tensor(input['index'], im)
        self.interpreter.invoke()
        self.output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        if YOLOV8:
            self.output_data if isinstance(self.output_data, np.ndarray) else self.output_data.numpy()
            self.output_data = np.squeeze(self.output_data[0])
        
        self.detect_started = True
            
    def detect(self, img, conf_thres=0.25, iou_thres=0.45):
        self.img = img.copy()
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.stopped = False
        if not self.thread_detect:
            self.detection_process()
        else:
            time.sleep(0.05)
            pass

        preprocess_info = (self.ratio, self.dwdh)
        return self.output_data, preprocess_info

