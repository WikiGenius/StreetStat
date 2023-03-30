# Author: Muhammed Elyamani
# Date: 03/02/2023
# GitHub: https://github.com/WikiGenius

from utils.layout import *
from utils import StyleApp
import utils
import re
import time
from kivy.core import window


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
        self.process = utils.Process(self.screen, self.pattern) 

        
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
 
    def process_after_video(self):
        self.stop_analyse()

    def stop_analyse(self):

        self.fps = 33
    
if __name__ == '__main__':
    StreetStat().run()
    
