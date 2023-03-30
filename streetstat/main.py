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

if platform !='android':
    Window.size = (400, 800)
    

class Matty(FloatLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)


class StreetStat(StyleApp):
    if DEBUG:
        DEBUG = DEBUG  
        KV_FILES = ["./streetstat.kv"]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Load YOLOv8n model for object detection
        self.pattern = re.compile(r'\d+')
        
  
    def on_start(self): 
        
        # Create initial bar chart
        self.create_init_bar(size_bar = 6)
        self.process = utils.Process(self.screen, self.pattern, self.canvas,  self.fig, self.ax, self.size_bar ) 
        
    def on_stop(self):
        # Stop the detector when the app is closed
        pass  
    
    def analyse_image(self, frame):
        self.process.visualize = self.screen.vis.active

        process_time = time.time()
        frame_vis = self.process.detect_traffic(frame.copy())
        
        process_time = time.time() - process_time
        self.fps = 1 / process_time
        return frame_vis
    
        
    def analyse_button(self):
        if self.start == False: 
            self.start = True
            text = self.screen.analyse_button.text.replace("ANALYZE", "STOP")
            self.screen.analyse_button.text = text
            
        else:
            self.start = False
            text = self.screen.analyse_button.text.replace("STOP", "ANALYZE")
            self.screen.analyse_button.text = text
            self.stop_analyse()
    def save_button(self):
        pass
 
 
    def create_init_bar(self, size_bar = 6):
        box_plot = self.screen.box_plot
        self.size_bar = size_bar
        fig, ax = plt.subplots()
        # fig.set_size_inches(8, 6)
        
        # Adjust the padding of the plot
        fig.subplots_adjust(bottom=0.2)
        self.fig, self.ax = create_figure_bar(fig, ax)
        
        self.canvas = FigureCanvasKivyAgg(self.fig)
        box_plot.add_widget(self.canvas)
        x = np.arange(size_bar)
        y = np.random.randint(1, 10, size=size_bar)
        self.ax.bar(x, y)
    def process_after_video(self):
        self.stop_analyse()

    def stop_analyse(self):

        self.fps = 33
    
if __name__ == '__main__':
    StreetStat().run()
    
