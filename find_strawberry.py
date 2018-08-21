# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 04:31:18 2017

@author: KARAN KHANNA
"""
#from _future_ import division

import cv2
import matplotlib as plt
import numpy as np
from math import cos,sin

green = (0,255,0)
def show(image):
    plt.figure = (10,10)
    plt.imshow(image, interpolation = 'nearest')

def overlay_mask(image):
    rgb_mask= cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    img = cv2.addWeighted(rgb_mask, 0.5, image, 0.5, 0)
    return img
    
def find_biggest_contour(image):
     image = image.copy()
     contours, hierarchy = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
     contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
     biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]

     mask = np.zeros(image.shape, np.uint8)
     cv2.drawContours(mask, [biggest_contour], -1, 255, -1)
     return biggest_contour, mask

def circle_contour(image, contour):
    image_with_ellipse = image.copy()
    ellipse = cv2.fitEllipse(contour)
    cv2.ellipse(image_with_ellipse, ellipse, green, 2, cv2.CV_AA)
    return image_with_ellipse

def find_strawberry(image):
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    max_dimension = max(image.shape)
    scale  = 700/max_dimension
    image = cv2.resize(image, None, fx = scale , fy = scale)
    blur = cv2.GaussianBlur(image, (7,7), 0)
    blur_hsv = cv2.cvtColor(blur ,cv2.COLOR_RGB2HSV)
    min_red = np.array([0 , 100 ,80])
    max_red = np.array([10,256,256])
    mask1 = cv2.inRange(blur_hsv, min_red , max_red)
    min_red_brightness = np.array([170 , 100 ,80])
    max_red_brightness = np.array([180,256,256])
    mask2 = cv2.inRange(blur_hsv, min_red_brightness,max_red_brightness )
    mask = mask1 + mask2
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15,15))
    mask_close = cv2.morphologyEx(mask, cv2.MORPH_CLOSE ,kernel)
    mask_open = cv2.morphologyEx(mask_close , cv2.MORPH_OPEN , kernel)
    
    biggest_strawberry_contour , mask_strawberry = find_biggest_contour(mask_open)
    overlay = overlay_mask(mask_open, image)
    circled = circle_contour(overlay,biggest_strawberry_contour)
    show(circled)
    bgr = cv2.cvtColor(circled, cv2.COLOR_RBG2BGR)
    return bgr
image = cv2.imread('strawberry.jpg')
result = find_strawberry(image)
cv2.imwrite('strawberry_result.jpg', result)

    
    
        
    
    
    
    