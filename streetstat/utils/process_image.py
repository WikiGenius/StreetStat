# Author: Muhammed Elyamani
# Date: 03/02/2023
# GitHub: https://github.com/WikiGenius

from conf import *
import utils
import numpy as np

class Process:
    def __init__(self, screen, pattern):
        self.screen = screen
        self.pattern = pattern
        self.visualize = False
        
    def detect_traffic(self, frame):
        conf_thres = self.screen.conf_thres.value / 100
        iou_thres = self.screen.iou_thres.value / 100
        
        dets, frame_info = detector.detect(frame, conf_thres=conf_thres, iou_thres=iou_thres)
        frame_vis = utils.draw_traffic(frame, dets, visualize=self.visualize )


        # Update GUI

        return frame_vis
