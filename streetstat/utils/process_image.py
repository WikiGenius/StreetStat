# Author: Muhammed Elyamani
# Date: 03/02/2023
# GitHub: https://github.com/WikiGenius

from conf import *
import utils
import numpy as np
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

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
        self.update_bar()
        
        return frame_vis
    def update_bar(self):
        x = [1,2,3,4,5]
        y = [6, 12, 6,9,15]

        plt.plot(x, y)
        plt.ylabel('Y Axis')
        plt.xlabel('X Axis')
        box_plot = self.screen.box_plot
        box_plot.add_widget(FigureCanvasKivyAgg(plt.gcf()))