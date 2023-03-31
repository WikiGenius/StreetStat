# Author: Muhammed Elyamani
# Date: 03/02/2023
# GitHub: https://github.com/WikiGenius

from asone.utils.draw import *
def draw_traffic(img, dets, visualize = True, identities=None, draw_trails=False, offset=(0, 0), class_names=None, filter_classes=None):
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


def bgr_to_hex(bgr):
    """Converts an RGB tuple to a hex string."""
    b, g, r = bgr
    return "#{:02x}{:02x}{:02x}".format(r, g, b)