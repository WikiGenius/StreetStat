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
        self.max_frames = MAX_FRAMES # Maximum number of frames to keep track of
        self.frame_counts = [] # List of lists to store counts for each object class for each frame
        self.bar_plots = []
        self.bar_index = []
        self.T = 0

    def detect_traffic(self, frame):
        conf_thres = self.screen.conf_thres.value / 100
        iou_thres = self.screen.iou_thres.value / 100
        self.bar_plots = []
        dets, frame_info = detector.detect(frame, conf_thres=conf_thres, iou_thres=iou_thres)
        frame_vis = utils.draw_traffic(frame, dets, visualize=self.visualize)

        # Generate random counts for each object class for this frame
        counts = [random.randint(1, 40) for _ in range(self.n_classes)]
        self.T +=1

        # Append counts for this frame to the list of frame counts
        self.frame_counts.append(counts)

        # Remove oldest frame if maximum number of frames is reached
        if len(self.frame_counts) > self.max_frames:
            self.frame_counts.pop(0)

        # Update bar chart with counts for each object class for each frame
        self.bar_index.append(len(self.bar_index))
        if len(self.bar_index) > self.max_frames:
            self.bar_index.pop(0)
        self.update_bar()
        return frame_vis

    def update_bar(self):
        # Update bar chart with new data
        self.ax.clear()

        create_figure_bar(self.fig, self.ax)

        # Iterate over each object class and each frame
        for i in range(self.n_classes):
            counts = [frame_counts[i] for frame_counts in self.frame_counts] # Get counts for object class i for all frames
            bp = self.ax.bar(np.arange(len(self.bar_index)) + (i * self.bar_width), 
                              counts, self.bar_width, alpha=BAR_OPACITY, 
                              color=colors[i], label=classes[i], linewidth=1)
            self.bar_plots.append(bp)


        self.ax.set_xticks(np.arange(len(self.bar_index)) + ((self.n_classes - 1) * self.bar_width / 2))

        # self.ax.set_xticklabels([str(i) for i in range(len(self.bar_index))])
        self.ax.set_xticklabels([str(i) for i in range(self.T)[-self.n_classes:]])
        self.ax.legend()
        self.canvas.draw()
