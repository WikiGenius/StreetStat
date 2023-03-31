# Author: Muhammed Elyamani
# Date: 03/02/2023
# GitHub: https://github.com/WikiGenius

import cv2
import asone
from ultralytics import YOLO
import numpy as np
detector = asone.ASOne(detector=asone.YOLOV8N_PYTORCH ,use_cuda=True)

DEBUG=True

classes = ['PERSON', 'CAR', 'MOTORCYCLE', 'BUS', 'TRUCK']
colors = ["#F63D54", "#027FFF", "#8876FE", "#0D1386", "#3C44C3"]

n_classes = len(classes)
n_groups = 6
bar_index = np.arange(n_groups)
bar_width = 0.15
bar_opacity = 0.8