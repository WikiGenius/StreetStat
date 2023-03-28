# Author: Muhammed Elyamani
# Date: 03/02/2023
# GitHub: https://github.com/WikiGenius

import os
from utils.layout import *


class StyleApp(MDApp):
    theme_cls = ThemeManager()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = "Dark"
        self.start = False
        self.fps = 33
        self.frame_count = 0
        
    def build(self):
        # Create instance of MainScreen
        self.screen = MainScreen(name='main')
        # Return the instance of MainScreen
        return self.screen
    
    def analyse_image(self, frame):
        return frame
    def process_after_video(self):
        pass
    def update(self, *args):
        # Read a frame from the video capture device
        ret, frame = self.capture.read()
        # Stop the detector if there are no more frames
        if not ret:
            # self.screen.detection_image.source = './data/upload.png'
            self.screen.detection_image.opacity = 0.1
            self.process_after_video()
            return
        frame = resize(frame, height=600)
    
        # Perform object detection on the frame using the YOLOv8n model
        if self.start:
            frame = self.analyse_image(frame)
        frame = create_rounded_img(frame, border_radius=40)
        
        cv2.line(frame, (20, 25), (127, 25), [85, 45, 255], 30)
        cv2.putText(frame, f'FPS: {int(self.fps)}', (11, 35), 0, 1, [
                    225, 255, 255], thickness=2, lineType=cv2.LINE_AA)
        # Flip the frame vertically for display purposes
        buf = cv2.flip(frame, 0).tobytes()
        # Create a Kivy Texture from the frame
        
        img_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        img_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            

        # Update the image in SearchDashboard with the new frame
        self.screen.detection_image.texture = img_texture
        self.screen.detection_image.opacity = 1
        # Increment frame count
        self.frame_count += 1
        # Clock.schedule_once(self.update)
        
            
    def upload_video(self):
        '''
        Call plyer filechooser API to run a filechooser Activity.
        '''
        # filters = [ '*.mp4']  # add more video file extensions here
        filters = [ '*.mkv']  # add more video file extensions here
        path = './assets/videos/*'
        filechooser.open_file(filters=filters, on_selection=self.handle_selection, path=path)

    def handle_selection(self, selection):
        '''
        Callback function for handling the selection response from Activity.
        '''
        if selection is not None:
            self.selection = selection
            print("Uploading video...")
            # Load the selected video file
            self.start_app(self.selection[0])


    def start_app(self, vid_path):
        # Create a video capture object for the selected video file
        print(f'load file: {vid_path}')
        print(f'file exist: {os.path.isfile(vid_path)}')
        self.capture = cv2.VideoCapture(vid_path)
        # Schedule the update function to be called at 33 FPS
        Clock.schedule_interval(self.update, 1/self.fps)
        # Clock.schedule_once(self.update)

if __name__ == '__main__':
    StyleApp().run()
