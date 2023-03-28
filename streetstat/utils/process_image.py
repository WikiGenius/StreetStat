# Author: Muhammed Elyamani
# Date: 03/02/2023
# GitHub: https://github.com/WikiGenius

from conf import *
import utils
import numpy as np

class Process:
    def __init__(self, screen, pattern):
        self.screen = screen
        self.pattern = pattern
        self.visualize = False
        
    def count_people(self, frame):
         conf_thres = self.screen.conf_thres.value / 100
         iou_thres = self.screen.iou_thres.value / 100
         face_thres = self.screen.face_thres.value / 100
         dets, frame_info = detector.detect(frame, conf_thres=conf_thres, iou_thres=iou_thres, input_shape=imgsz)
         frame, count_people, faceBoxes, faceScores = utils.draw_count_people(frame, dets, visualize=self.visualize, conf_thresh_face=face_thres )

         selected_faceBoxes, selected_faceScores = self.get_top_k_face(faceBoxes, faceScores, k = TOP_K_FACES)

         people_count_number = self.screen.people_count.text
         modified_people_count_number = self.pattern.sub(f"{count_people}", people_count_number)
         self.screen.people_count.text = modified_people_count_number

         return frame, selected_faceBoxes

    def analyse_faces(self, frame, frame_vis, faceBoxes):
        total_ages = 0
        total_genderList = []
        for faceBox in faceBoxes:
            face = utils.preprocess_face(frame, faceBox)

            gender, age=utils.predict_age_gender(face)
            
            total_genderList.append(gender)
            
            ag1, age2 = age.strip('()').split('-')
            total_ages += (int(ag1) + int(age2)) / 2
            
            frame_vis = utils.draw_analyse_faces(self.screen, self.pattern, frame_vis, gender, age, faceBoxes, faceBox, self.visualize, total_genderList, total_ages, eps_size= EPS_SIZE)
        
        return frame_vis
    
    def get_top_k_face(self, faceBoxes, faceScores, k = 5):
        indeces = np.argsort(faceScores)[-k:]
        selected_faceBoxes = faceBoxes[indeces]
        selected_faceScores = faceScores[indeces]
        return selected_faceBoxes, selected_faceScores