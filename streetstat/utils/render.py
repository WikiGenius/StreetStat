# Author: Muhammed Elyamani
# Date: 03/02/2023
# GitHub: https://github.com/WikiGenius

import cv2
import numpy as np

def create_rounded_img(img, border_radius = 50):
    # get the width and height of the image
    h, w = img.shape[:2]

    # create a mask with same height and width of the original image 
    mask = np.zeros((h,w), np.uint8)

    # Draw a rounded rectangle
    rect_color = (255, 255, 255)
    rect_top_left = (0, 0)
    rect_bottom_right = (w, h)
    cv2.rectangle(mask, (rect_top_left[0] + border_radius, rect_top_left[1]), (rect_bottom_right[0] - border_radius, rect_bottom_right[1]), rect_color, -1)
    cv2.rectangle(mask, (rect_top_left[0], rect_top_left[1] + border_radius), (rect_bottom_right[0], rect_bottom_right[1] - border_radius), rect_color, -1)
    cv2.circle(mask, (rect_top_left[0] + border_radius, rect_top_left[1] + border_radius), border_radius, rect_color, -1)
    cv2.circle(mask, (rect_bottom_right[0] - border_radius, rect_top_left[1] + border_radius), border_radius, rect_color, -1)
    cv2.circle(mask, (rect_top_left[0] + border_radius, rect_bottom_right[1] - border_radius), border_radius, rect_color, -1)
    cv2.circle(mask, (rect_bottom_right[0] - border_radius, rect_bottom_right[1] - border_radius), border_radius, rect_color, -1)
    # Apply the mask to the image
    masked_image = cv2.bitwise_and(img, img, mask=mask)

    # Create a black background image with the same height and width of the original image
    background = np.zeros((h, w, 3), np.uint8)

    # Invert the mask
    mask_inv = cv2.bitwise_not(mask)

    # Apply the inverted mask to the background image
    background = cv2.bitwise_and(background, background, mask=mask_inv)

    # Combine the masked image and the background using addWeighted
    alpha = 1
    beta = 0
    gamma = 0
    rounded_img = cv2.addWeighted(masked_image, alpha, background, beta, gamma)
    return rounded_img

