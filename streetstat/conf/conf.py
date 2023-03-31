# Author: Muhammed Elyamani
# Date: 03/02/2023
# GitHub: https://github.com/WikiGenius

import cv2
import asone
from ultralytics import YOLO

detector = asone.ASOne(detector=asone.YOLOV8N_PYTORCH ,use_cuda=True)

DEBUG=True

classes = ['PERSON', 'CAR', 'MOTORCYCLE', 'BUS', 'TRUCK']
colors = ["#F63D54", "#027FFF", "#8876FE", "#0D1386", "#3C44C3"]