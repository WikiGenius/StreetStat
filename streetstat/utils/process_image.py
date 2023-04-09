# Author: Muhammed Elyamani
# Date: 03/02/2023
# GitHub: https://github.com/WikiGenius

from conf import *
import utils
import numpy as np
from utils.layout import create_figure_bar
from threading import Thread
import time

class Process:
    def __init__(self, screen, pattern, canvas, fig, ax):
        self.screen = screen
        self.pattern = pattern
        self.visualize = False
        self.canvas = canvas
        self.fig = fig
        self.ax = ax
        self.get_classes()
 
        self.max_frames = MAX_FRAMES # Maximum number of frames to keep track of
        self.frame_counts = [] # List of lists to store counts for each object class for each frame
        self.counts_dict = dict()
        self.bar_plots = []
        self.bar_index = []
        self.T = 0
        
        if not PLATFORM_ANDROID:
            import asone
            self.detector = asone.ASOne(detector=asone.YOLOV8N_PYTORCH ,use_cuda=True)
        else:
            from model_tflite import Detector
            self.detector = Detector(model_tflite_path)
        
        # Variable to control multi threads
        self.stopped = False
        self.start_process = False
        self.traffic_process_started = False
    def start(self):
        # Start the thread that update_detection
        Thread(target=self.update_process, args=(), daemon=True).start()
        return self

    def stop(self):
        # Indicate that the camera and thread should be stopped
        self.stopped = True
        
    def update_process(self):
        while not self.stopped:
            if self.start_process:
                self.traffic_process()
    
    def traffic_process(self):

        self.conf_thres = self.screen.conf_thres.value / 100
        self.iou_thres = self.screen.iou_thres.value / 100
        self.get_classes()
        self.dets, self.frame_info = self.detector.detect(self.frame, conf_thres=self.conf_thres, iou_thres=self.iou_thres)
        
        self.traffic_process_started = True    
         
    def detect_traffic(self, frame, start):
        self.frame = frame.copy()
        self.start_process = start   
        self.stopped = False
        self.T +=1
        
        if self.T % SKIP_FRAMES != 0:
            return self.frame, self.counts_dict, self.T, self.frame_counts    
        if not THREAD:
            self.traffic_process()
        else:
            # time.sleep(0.05)
            pass
        if self.traffic_process_started: 
            self.frame, self.counts_dict, self.colors_dict = utils.draw_traffic(self.frame, self.frame_info, self.dets, visualize=self.visualize, filter_classes=self.classes, conf_thres = self.conf_thres )

            counts = list(self.counts_dict.values())
            self.colors = list(self.colors_dict.values())
            # Append counts for this frame to the list of frame counts
            self.frame_counts.append(counts)
            # Remove oldest frame if maximum number of frames is reached
            if len(self.frame_counts) > self.max_frames:
                self.frame_counts.pop(0)
            # Update bar chart with counts for each object class for each frame
            self.bar_index.append(len(self.bar_index))
            if len(self.bar_index) > self.max_frames:
                self.bar_index.pop(0)
            try:
                self.update_bar()
            except Exception as e:
                print(f"Exception: {e}")
                self.reset_bar_chart()
        if len(self.frame_counts) > 0 and len(self.frame_counts[0]) != len(self.counts_dict.keys()):
             self.reset_bar_chart()

        return self.frame, self.counts_dict, self.T, self.frame_counts

    def update_bar(self):
        # Update bar chart with new data
        self.ax.clear()
        self.bar_plots = []

        create_figure_bar(self.fig, self.ax)
        labels = [str(i) for i in range(0, self.T, SKIP_FRAMES)[-MAX_FRAMES:]]
        # Iterate over each object class and each frame
        for i in range(self.n_classes):
            counts = [frame_counts[i] for frame_counts in self.frame_counts] # Get counts for object class i for all frames
            if not self.colors[i]:
                continue
            bp = self.ax.bar(np.arange(len(self.bar_index)) + (i * self.bar_width), 
                              counts, self.bar_width, alpha=BAR_OPACITY, 
                              color=self.colors[i], label=self.classes[i], linewidth=1)
            self.bar_plots.append(bp)
            
        
        x_ticks = np.arange(len(self.bar_index)) + ((self.n_classes - 1) * self.bar_width / 2)
        
        self.ax.set_xticks(x_ticks)

        self.ax.set_xticklabels(labels)

        # self.ax.legend()
        # self.ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        self.canvas.draw()

    def reset_bar_chart(self):
        self.frame_counts = [] # List of lists to store counts for each object class for each frame
        self.bar_plots = []
        self.bar_index = []
        self.T = 0
        self.ax.clear()
        create_figure_bar(self.fig, self.ax)
        pass

    def get_classes(self):
        self.classes = []
        self.classes.append('PERSON') if self.screen.person_checkbox.active else None
        self.classes.append('CAR') if self.screen.car_checkbox.active else None
        self.classes.append('MOTORCYCLE') if self.screen.motorcycle_checkbox.active else None
        self.classes.append('BUS') if self.screen.bus_checkbox.active else None
        self.classes.append('TRUCK') if self.screen.truck_checkbox.active else None
        
        self.n_classes = len(self.classes)
        if  self.n_classes != 0 :
            self.bar_width = 0.9 / self.n_classes
        else:
            self.bar_width  = 0