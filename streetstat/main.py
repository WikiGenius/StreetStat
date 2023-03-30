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

class StreetStat(StyleApp):
    if DEBUG:
        DEBUG = DEBUG  
        KV_FILES = ["./streetstat.kv"]

if __name__ == '__main__':
    StreetStat().run()
    
