# Author: Muhammed Elyamani
# Date: 03/02/2023
# GitHub: https://github.com/WikiGenius

from conf import *

def bgr_to_hex(bgr):
    """Converts an RGB tuple to a hex string."""
    b, g, r = bgr
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

# import platform
if not PLATFORM_ANDROID:
    from asone.utils.draw import *
    
    def draw_traffic(img, frame_info, dets, visualize = True, filter_classes=None, conf_thres=0.25, identities=None, draw_trails=False, offset=(0, 0), class_names=None):
        counts_dict = {cls.lower(): 0 for cls in filter_classes}
        colors_dict = {cls.lower(): None for cls in filter_classes}
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

                if label not in counts_dict.keys():
                    continue
                counts_dict[label] += 1
                if not colors_dict[label]:
                    colors_dict[label] = bgr_to_hex(color)

                if visualize:
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

        return img, counts_dict, colors_dict
else:
    import cv2
    import numpy as np
    import utils
    import random

    
    palette = (2 ** 11 - 1, 2 ** 15 - 1, 2 ** 20 - 1)
    data_deque = {}
    def draw_traffic(img, frame_info, dets, visualize = True, filter_classes=None, conf_thres=0.25, identities=None, draw_trails=False, offset=(0, 0), class_names=None):
         
        ratio, dwdh = frame_info
        output_data = dets
        if YOLOV8:
            img, counts_dict, colors_dict = draw_boxes_v8(img, ratio, dwdh, output_data, conf_thres, filter_classes, visualize)
        else:
            img, counts_dict, colors_dict = draw_boxes_vn(img, ratio, dwdh, output_data, conf_thres, filter_classes, visualize)

        return img, counts_dict, colors_dict


    def draw_boxes_v8(img, ratio, dwdh, output_data, conf_thres=0.25, filter_classes=None, visualize=True):
        output_data = np.transpose(output_data)
        scores = output_data[:, 4:]
        boxes = output_data[:, :4]
        
        counts_dict = {cls.lower(): 0 for cls in filter_classes}
        colors_dict = {cls.lower(): None for cls in filter_classes}
        
        for i,(cx,cy,w,h) in enumerate(boxes):
            x0 = cx - w /2
            y0 = cy - h /2
            x1=x0+w
            y1=y0+h

            cls_id = np.argmax(scores[i])
            score = scores[i][cls_id]
            cls_id = int(cls_id)
            name = utils.NAMES[cls_id]
            score = round(float(score),3)

            if filter_classes and name in filter_classes and score > conf_thres:
                counts_dict[name] += 1
                if not colors_dict[name]:
                    colors_dict[name] = bgr_to_hex(color)
                    
                box = np.array([x0,y0,x1,y1])
                box -= np.array(dwdh*2)
                box /= ratio
                box = box.round().astype(np.int32).tolist()

                #Creating random colors for bounding box visualization.
                color = compute_color_for_labels(cls_id)
                name = f"{name}  {score}"


                if visualize:
                    draw_ui_box(box, img, label=name, color=color, line_thickness=2)    
        return img, counts_dict, colors_dict



    def draw_boxes_vn(img, ratio, dwdh, output_data, conf_thres=0.25, filter_classes=None, visualize=True):
        counts_dict = {cls.lower(): 0 for cls in filter_classes}
        colors_dict = {cls.lower(): None for cls in filter_classes}
        
        for i,(batch_id,x0,y0,x1,y1,cls_id,score) in enumerate(output_data):
            cls_id = int(cls_id)
            name = utils.NAMES[cls_id]
            score = round(float(score),2)

            if filter_classes and name in filter_classes and score > conf_thres:
                counts_dict[name] += 1
                if not colors_dict[name]:
                    colors_dict[name] = bgr_to_hex(color)
                    
                box = np.array([x0,y0,x1,y1])
                box -= np.array(dwdh*2)
                box /= ratio
                box = box.round().astype(np.int32).tolist()

                #Creating random colors for bounding box visualization.
                color = compute_color_for_labels(cls_id)
                name = f"{name}  {score}"
                if visualize:
                    draw_ui_box(box, img, label=name, color=color, line_thickness=2)    
        return img, counts_dict, colors_dict

    def draw_ui_box(x, img, label=None, color=None, line_thickness=None):
        # Plots one bounding box on image img
        tl = line_thickness or round(
            0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
        color = color or [random.randint(0, 255) for _ in range(3)]
        c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
        cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)

        if label:
            tf = max(tl - 1, 1)  # font thickness
            t_size = cv2.getTextSize(str(label), 0, fontScale=tl / 3, thickness=tf)[0]
            # c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
            img = draw_border(img, (c1[0], c1[1] - t_size[1] - 3),
                              (c1[0] + t_size[0], c1[1]+3), color, 1, 8, 2)

            # cv2.line(img, c1, c2, color, 30)
            # cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
            cv2.putText(img, str(label), (c1[0], c1[1] - 2), 0, tl / 3,
                        [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)


    def draw_border(img, pt1, pt2, color, thickness, r, d):
        x1, y1 = pt1
        x2, y2 = pt2
        # Top leftfrom collections import deque (x1, y1 + r + d), color, thickness)
        cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)

        # Top right
        cv2.line(img, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
        cv2.line(img, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
        cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)
        # Bottom left
        cv2.line(img, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
        cv2.line(img, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
        cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)
        # Bottom right
        cv2.line(img, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
        cv2.line(img, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
        cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)

        cv2.rectangle(img, (x1 + r, y1), (x2 - r, y2), color, -1, cv2.LINE_AA)
        cv2.rectangle(img, (x1, y1 + r), (x2, y2 - r - d), color, -1, cv2.LINE_AA)

        cv2.circle(img, (x1 + r, y1+r), 2, color, 12)
        cv2.circle(img, (x2 - r, y1+r), 2, color, 12)
        cv2.circle(img, (x1 + r, y2-r), 2, color, 12)
        cv2.circle(img, (x2 - r, y2-r), 2, color, 12)

        return img



    def drawtrails(data_deque, id, color, img):
        # draw trail
        for i in range(1, len(data_deque[id])):
            # check if on buffer value is none
            if data_deque[id][i - 1] is None or data_deque[id][i] is None:
                continue

            # generate dynamic thickness of trails
            thickness = int(np.sqrt(64 / float(i + i)) * 1.5)

            # draw trails
            cv2.line(img, data_deque[id][i - 1], data_deque[id][i], color, thickness)



    def compute_color_for_labels(label):
        """
        Simple function that adds fixed color depending on the class
        """
        if label == 0:  # person  #BGR
            color = (85, 45, 255)
        elif label == 2:  # Car
            color = (222, 82, 175)
        elif label == 3:  # Motobike
            color = (0, 204, 255)
        elif label == 5:  # Bus
            color = (0, 149, 255)
        else:
            color = [int((p * (label ** 2 - label + 1)) % 255) for p in palette]
        return tuple(color)

