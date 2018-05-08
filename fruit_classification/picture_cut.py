# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 15:27:46 2018

@author: hp
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt



def process(path):

    def get_image(path):
        img=cv2.imread(path)

        return img
    def image_size(img):
        w,h=img.shape[:2]
        area=w*h
        return area
    def gray_image(img):

        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        return gray

    def thresh_img(img,i=1):

        if i==1:
            blur=cv2.GaussianBlur(img,(9,9),0)
        if i==2:
            blur=cv2.medianBlur(img,3)

        thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,9,0)

        return thresh
    def get_strcture(img):
        kernel=np.ones((3,3),np.uint8)
        #kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(25,25))
        closed=cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,kernel,iterations=5)
        opening=cv2.morphologyEx(closed,cv2.MORPH_OPEN,kernel,iterations=10)
        sure_bg=cv2.dilate(opening,kernel,iterations=5)
        return sure_bg

    def bitwise_and(img,mask):

        image=cv2.bitwise_and(img,img,mask=mask)
        return image

    def back_delete(img):
        kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        close=cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernel)
        div=np.float32(img)/(close)
        res=np.uint8(cv2.normalize(div,div,0,255,cv2.NORM_MINMAX))
        return res

    def find_contours(img):
        (_,cnts, _) = cv2.findContours(img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        return cnts

    def resize(img):
        return cv2.resize(img,(500,500),interpolation=cv2.INTER_CUBIC)

    def choice_p(cnts):
        contour=[]
        for i in range(len(cnts)):
            if cv2.contourArea(cnts[i])>0.1*area:
                contour.append(cnts[i])
        return contour


    #path = './test2.jpg'
    img_original = get_image(path)
    #img_original=resize(img_original)
    area = image_size(img_original)
    res = back_delete(img_original)


    gray = gray_image(res)

    thresh = thresh_img(gray)
    opening = get_strcture(thresh)
    image = bitwise_and(img_original,opening)
    gray2 = gray_image(image)

    thresh2 = thresh_img(gray2)

    closed = get_strcture(thresh2)
    cnts=find_contours(closed)
    contour = choice_p(cnts)
    temp_img = img_original
    for i in range(len(contour)):

        x, y, w, h = cv2.boundingRect(contour[i])
        cv2.rectangle(temp_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        img2 = temp_img[y:y+h,x:x+w]
        '''
        rect=cv2.minAreaRect(cnts[i])
        box=cv2.boxPoints(rect)
        box=np.int0(box)
        cv2.drawContours(temp_img,[box],0,(0,0,255),2)
        '''
    return img2

if __name__ == "__main__":
    path2 = './test2.jpg'
    img2 = process(path2)

    cv2.imshow('a',img2)
    #cv2.imshow('a',temp_img)
    cv2.imwrite('final.jpg',img2)

    cv2.waitKey()
