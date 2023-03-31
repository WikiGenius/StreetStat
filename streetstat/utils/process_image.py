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
    def __init__(self, screen, pattern, canvas, fig, ax):
        self.screen = screen
        self.pattern = pattern
        self.visualize = False
        self.canvas = canvas
        self.fig = fig
        self.ax = ax
        self.n_classes = len(classes)
        self.bar_width = 0.9 / self.n_classes
        # self.bar_index = np.arange(len(pattern)) * self.n_classes * self.bar_width
        self.bar_index =  bar_index
        self.bar_plots = []

    def detect_traffic(self, frame):
        conf_thres = self.screen.conf_thres.value / 100
        iou_thres = self.screen.iou_thres.value / 100
        self.bar_plots = []
        dets, frame_info = detector.detect(frame, conf_thres=conf_thres, iou_thres=iou_thres)
        frame_vis = utils.draw_traffic(frame, dets, visualize=self.visualize)

        # Update GUI
        counts = [random.randint(1, 40) for _ in range(self.n_classes)]
        self.update_bar(counts)

        return frame_vis

    def update_bar(self, counts):
        # Update bar chart with new data
        self.ax.clear()

        create_figure_bar(self.fig, self.ax)

        for i in range(self.n_classes):
            bp = self.ax.bar(self.bar_index + (i * self.bar_width), counts[i], 
                             self.bar_width, alpha=bar_opacity, color=colors[i], label=classes[i])
            self.bar_plots.append(bp)

        self.ax.set_xlabel('Frames')
        self.ax.set_ylabel('Count')
        self.ax.set_title('Object Count per Frame')
        self.ax.set_xticks(self.bar_index + ((self.n_classes - 1) * self.bar_width / 2))
        self.ax.set_xticklabels([str(i) for i in range(len(self.bar_index))])
        self.ax.legend()
        self.canvas.draw()
