# Author: Muhammed Elyamani
# Date: 03/02/2023
# GitHub: https://github.com/WikiGenius

from conf import *
import utils
import numpy as np
import matplotlib.pyplot as plt
from utils.layout import create_figure_bar
import random
class Process:
    def __init__(self, screen, pattern, canvas,  fig, ax ):
        self.screen = screen
        self.pattern = pattern
        self.visualize = False
        self.canvas = canvas
        self.fig = fig
        self.ax = ax 
        self.size_bar = len(classes)
        
    def detect_traffic(self, frame):
        conf_thres = self.screen.conf_thres.value / 100
        iou_thres = self.screen.iou_thres.value / 100
        
        dets, frame_info = detector.detect(frame, conf_thres=conf_thres, iou_thres=iou_thres)
        frame_vis = utils.draw_traffic(frame, dets, visualize=self.visualize )
        

        # Update GUI
        counts = [random.randint(1, 40) for _ in range(len(classes))]
        
        self.update_bar(counts)
        
        return frame_vis
    def update_bar(self, counts):
        # Update bar chart with new data
        x = np.arange(self.size_bar)
        y = np.random.randint(1, 10, size=self.size_bar)
        self.ax.clear()
    
        create_figure_bar(self.fig, self.ax)
        bars = self.ax.bar(x, counts, color=colors)

        for i, bar in enumerate(bars):
            bar.set_label(classes[i])
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(classes, rotation=50)
        self.ax.bar(x, y)
        self.canvas.draw()