# Author: Muhammed Elyamani
# Date: 03/02/2023
# GitHub: https://github.com/WikiGenius

# Import necessary packages
from conf import *
import matplotlib.pyplot as plt
from kivy import platform
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.slider import MDSlider
import cv2
from kivymd.theming import ThemeManager
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from utils import resize, create_rounded_img
from plyer import filechooser
import random
import numpy as np


if DEBUG:
    from kivymd.tools.hotreload.app import MDApp
else:
    from kivymd.app import MDApp

# importing labelbase which
# register our custom font for application
from kivy.core.text import LabelBase
# registering our new custom fontstyle
LabelBase.register(name='Montserrat',
                   fn_regular='assets/fonts/Montserrat/static/Montserrat-Black.ttf')


class Myslider(MDSlider):
    def on_touch_up(self, touch):
        self.active = True

# Define the main widget for the app
class MainScreen(Screen):
    pass       

    
def create_figure_bar(fig, ax):
    ax.set_xlabel('Time (S)')
    ax.set_ylabel('Count')
    ax.set_title('Object Count per Sec')
    # ax.legend()
    return fig, ax
