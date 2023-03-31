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
# colors = ["#F63D54", "#027FFF", "#8876FE", "#0D1386", "#3C44C3"]

BAR_OPACITY = 0.8
MAX_FRAMES = 5