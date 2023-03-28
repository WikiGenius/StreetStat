import cv2
from conf import *

def fix_square(faceBox):
    w = faceBox[2] - faceBox[0]
    h = faceBox[3] - faceBox[1]
    # print(f"before fixing square: {w} X {h}")
    
    padding_fix_square = abs(w - h) // 2
    if w < h:
        faceBox[0] -= padding_fix_square
        faceBox[2] += padding_fix_square
    elif w > h:
        faceBox[1] -= padding_fix_square
        faceBox[3] += padding_fix_square
    
    w = faceBox[2] - faceBox[0]
    h = faceBox[3] - faceBox[1]
    # print(f"after fixing square: {w} X {h}")

    return faceBox, w

def preprocess_face(frame, faceBox):
    if FIX_SQUARE:
        faceBox, w = fix_square(faceBox)
        
    padding = int(PADDING * w)
    
    face=frame[max(0,faceBox[1]-padding):
           min(faceBox[3]+padding,frame.shape[0]-1),max(0,faceBox[0]-padding)
           :min(faceBox[2]+padding, frame.shape[1]-1)]
    # print(f"shape after padding: {face.shape}")
    face = cv2.resize(face, (128, 128))
    # print(f"new shape: {face.shape}")
    # print('===============================================')
    return face