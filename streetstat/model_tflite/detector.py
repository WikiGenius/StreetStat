# Author: Muhammed Elyamani
# Date: 03/02/2023
# GitHub: https://github.com/WikiGenius

from conf import YOLOV8
from threading import Thread
import model_tflite
import utils
import time
import numpy as np

class Detector:
    def __init__(self, model_tflite_path, use_cuda=False):        
        self.use_cuda = use_cuda
        self.interpreter, self.input_details, self.output_details = model_tflite.get_model(
            model_tflite_path)
        if YOLOV8:
            self.input_shape = self.input_details[0]['shape'][1:3]
        else:
            self.input_shape = self.input_details[0]['shape'][2:]
            
        self.output_data = []

    def detection_process(self):

        transpose=False
        if not YOLOV8:
            transpose = True
        im, self.ratio, self.dwdh = utils.preprocess(self.img, self.input_shape, transpose)
        
        # predict the model
        input = self.input_details[0]
        self.interpreter.set_tensor(input['index'], im)
        self.interpreter.invoke()
        self.output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        if YOLOV8:
            self.output_data if isinstance(self.output_data, np.ndarray) else self.output_data.numpy()
            self.output_data = np.squeeze(self.output_data[0])
        
    def detect(self, img, conf_thres=0.25, iou_thres=0.45):
        self.img = img.copy()
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.detection_process()

        preprocess_info = (self.ratio, self.dwdh)
        return self.output_data, preprocess_info

