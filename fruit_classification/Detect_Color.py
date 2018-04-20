# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 19:57:51 2018

@author: hp
"""

import cv2
import numpy as np

#image=cv2.imread('test5.jpg')

def Pix_Cont(image):
    cont=0
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    rows,cols=gray.shape
    for i in range(rows):
        for j in range(rows):
            if image[i,j,1]!=0 and image[i,j,1]!=0 and image[i,j,2]!=0:
                cont=cont+1
    return cont
def Detect_Color(image,color):

    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    if color=="yello":
        lower_yello=np.array([11,43,46])
        upper_yello=np.array([25,255,255])
        mask_yello=cv2.inRange(hsv,lower_yello,upper_yello)
        res_yello=cv2.bitwise_and(image,image,mask=mask_yello)
        yello_conts=Pix_Cont(res_yello)
        return yello_conts
    if color=="black":
        lower_black=np.array([0,0,0])
        upper_black=np.array([180,255,46])
        mask_black=cv2.inRange(hsv,lower_black,upper_black)
        res_black=cv2.bitwise_and(image,image,mask=mask_black)
        black_conts=Pix_Cont(res_black)
        return black_conts
    if color=="green":
        lower_green=np.array([35,43,46])
        upper_green=np.array([99,255,255])
        mask_green=cv2.inRange(hsv,lower_green,upper_green)
        res_green=cv2.bitwise_and(image,image,mask=mask_green)
        green_conts=Pix_Cont(res_green)
        return green_conts

def main():

    y = Detect_Color(image,"yello")
    b = Detect_Color(image,"black")
    g = Detect_Color(image,"green")
    print(y)
    print(b)
    print(g)

if __name__ == "__main__":
    main()
