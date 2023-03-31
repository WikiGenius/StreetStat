# Author: Muhammed Elyamani
# Date: 03/02/2023
# GitHub: https://github.com/WikiGenius

from utils.layout import *
from utils import StyleApp
import utils
import re
import time
from kivy.core import window
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import numpy as np
import random

if platform !='android':
    Window.size = (400, 800)
    
      
class StreetStat(StyleApp):
    if DEBUG:
        DEBUG = DEBUG  
        KV_FILES = ["./streetstat.kv"]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Load YOLOv8n model for object detection
        self.pattern = re.compile(r'\d+')
        self.counts_dict = {}
        self.T = 0
  
    def on_start(self): 
        
        # Create initial bar chart
        self.create_init_bar()
        self.process = utils.Process(self.screen, self.pattern, self.canvas,  self.fig, self.ax ) 
        
    def on_stop(self):
        # Stop the detector when the app is closed
        pass  
    
    def analyse_image(self, frame):
        self.process.visualize = self.screen.vis.active

        process_time = time.time()
        frame_vis, self.counts_dict, self.T = self.process.detect_traffic(frame.copy())

        process_time = time.time() - process_time
        self.fps = 1 / process_time
        return frame_vis
    
        
    def analyse_button(self):
        if self.start == False: 
            self.start = True
            text = self.screen.analyse_button.text.replace("ANALYZE", "STOP")
            self.screen.analyse_button.text = text
            self.screen.box_plot.opacity = 1
            
        else:
            self.start = False
            text = self.screen.analyse_button.text.replace("STOP", "ANALYZE")
            self.screen.analyse_button.text = text
            self.screen.box_plot.opacity = 0.1

            self.stop_analyse()
    def save_button(self):
        if len(self.counts_dict.values()) == 0:
            print('empty')
        else:
            print(self.counts_dict)
        pass
 

    def create_init_bar(self):
        box_plot = self.screen.box_plot
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        create_figure_bar(self.fig, self.ax)
        
        self.fig.subplots_adjust(bottom=0.2, left=0.17)

        self.canvas = FigureCanvasKivyAgg(self.fig)
        
        box_plot.add_widget(self.canvas)
        
    def process_after_video(self):
        self.stop_analyse()

    def stop_analyse(self):
        self.process.reset_bar_chart()
        self.T = 0
        self.counts_dict = {}
        self.fps = 33
    
if __name__ == '__main__':
    StreetStat().run()
    
