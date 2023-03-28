# Author: Muhammed Elyamani
# Date: 03/02/2023
# GitHub: https://github.com/WikiGenius

from asone.utils.draw import *
def draw_count_people(img, dets, visualize = True, identities=None, draw_trails=False, offset=(0, 0), class_names=['face', 'person'], conf_thresh_face = 0.25):
    count_people = 0
    faceBoxes = []
    faceScores = []
    if dets is not None: 
        bbox_xyxy = dets[:, :4]
        scores = dets[:, 4]
        class_ids = dets[:, 5]
        # cv2.line(img, line2[0], line2[1], (0,200,0), 3)
        height, width, _ = img.shape

        # remove tracked point from buffer if object is lost
        if draw_trails:
            for key in list(data_deque):
                if key not in identities:
                    data_deque.pop(key)
        for i, box in enumerate(bbox_xyxy):
            x1, y1, x2, y2 = [int(i) for i in box]
            x1 += offset[0]
            x2 += offset[0]
            y1 += offset[1]
            y2 += offset[1]
    
            # get ID of object
            id = int(identities[i]) if identities is not None else None
            
            # if class_ids is not None:
            color = compute_color_for_labels(int(class_ids[i]))
    
            if class_names:
                obj_name = class_names[int(class_ids[i])]
            else:                
                obj_name = names[int(class_ids[i])]
            
            label = f'{obj_name}' if id is None else f'{id}'
            if label == 'person':
               count_people += 1
               
            elif label == 'face':
                if scores[i] >= conf_thresh_face:
                    faceBoxes.append(get_face(box, offset))
                    faceScores.append(scores[i])
                
            if visualize:
                if label == 'person' or (label == 'face' and scores[i] >= conf_thresh_face):
                    draw_ui_box(box, img, label=label, color=color, line_thickness=2)
    
            # Draw trails        
            # code to find center of bottom edge
            center = (int((x2+x1) / 2), int((y2+y2)/2))
    
            if draw_trails and visualize:
                # create new buffer for new object
                if id not in data_deque:  
                    data_deque[id] = deque(maxlen= 64)
            
                data_deque[id].appendleft(center)    
                drawtrails(data_deque, id, color, img)
                
    faceBoxes = np.array(faceBoxes)
    faceScores = np.array(faceScores)
    return img, count_people, faceBoxes, faceScores 


def get_face(box, offset):
    x1, y1, x2, y2 = [int(i) for i in box]
    x1 += offset[0]
    x2 += offset[0]
    y1 += offset[1]
    y2 += offset[1]
    return [x1, y1, x2, y2]



def draw_analyse_faces(screen, pattern, frame_vis, gender, age, faceBoxes, faceBox, visualize, total_genderList, total_ages, eps_size = 0.05):
    color = compute_color_for_labels(5)
    if visualize:
        tl = round(0.002 * (frame_vis.shape[0] + frame_vis.shape[1]) / 2) + 1  # line/font thickness
        tf = max(tl - 1, 1)  # font thickness
        cv2.putText(frame_vis,  f'{gender}, {age}', (faceBox[0], faceBox[1] - 5), 0, tl / 3,
                    [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
    if faceBoxes.shape[0] > 0:
        avg_age = int(total_ages / faceBoxes.shape[0])
        M_count = sum([1 for x in total_genderList if x=='M' ])
        M_ratio = M_count /  len(total_genderList)
        if M_ratio == 0:
            M_ratio += eps_size
            
        elif M_ratio == 1:
            M_ratio -= eps_size
            
        F_ratio = 1 - M_ratio
        
    else:
        M_ratio = 0.5
        F_ratio = 0.5
        avg_age= 0
    if M_ratio < 0.3:
        screen.gender_M.text = ""
    else:
        screen.gender_M.text = "[font=Montserrat]M[/font]"
    if F_ratio < 0.3:
        screen.gender_F.text = ""
    else:
        screen.gender_F.text = "[font=Montserrat]F[/font]"
    
    
    screen.gender_M.size_hint_x =  M_ratio
    screen.gender_F.size_hint_x =  F_ratio
    
    avg_age_number = screen.avg_age.text
    modified_avg_age_number = pattern.sub(f"{avg_age}", avg_age_number)
    screen.avg_age.text = modified_avg_age_number
    
    return frame_vis