import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def plot_image(img, grayscale=True):
    img = cv2.imread("{}".format("Imagenes_autos/000.png/"))
    #print(img.shape)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(gray.shape)
    gray = cv2.blur(gray,(3,3))
    canny = cv2.Canny(gray,150,200)
    canny = cv2.dilate(canny,None,iterations=0)
    cnts,_ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(img,cnts,-1,(0,255,0),2)

    # for c in cnts:
    #     area = cv2.contourArea(c)
    #     x,y,w,h = cv2.boundingRect(c)
    #     epsilon = 0.05*cv2.arcLength(c,True)
    #     approx = cv2.approxPolyDP(c,epsilon,True)
    #     if len(approx)==4 and area > 5:
    #         print('area=', area)
    #         # cv2.drawContours(img,[c],0,(0,255,0),2)
    #         license_ratio = float(w)/h
    #         if license_ratio > 1.4:
    #             cv2.drawContours(img,[c],0,(0,255,0),2)

    # cv2.imshow('Image', img)
    cv2.imshow('Canny', canny)
    cv2.moveWindow('Canny',45,10)
    cv2.waitKey(0)
    # thresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY_INV)[1]
    # contours = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # license_ratio = 3.07692307692
    # min_w = 80
    # max_w = 110
    # min_h = 25
    # max_h = 52
    # candidates = []
    # for cnt in contours:
    #     x, y, w, h = cv2.boundingRect(cnt)
    #     aspect_ratio = float(w)/h
    #     if(np.isclose(aspect_ratio, license_ratio, atol = 0.7) and (max_w > w > min_w) and (max_h > h > min_h)):
    #         candidates.append(cnt)

    # ys = []
    # for cnt in candidates:
    #     x, y, w, h = cv2.boundingRect(cnt)
    #     ys.append(y)
    # license = candidates[np.argmax(ys)]

    # canvas = np.zeros_like(img)
    # cv2.drawContours(canvas, contours, -1, (0,255,0), 2)
    # plt.axis('off')
    # plt.imshow(canvas)

def main():

    img = cv2.imread(f"Imagenes_autos/000.png/")
    plot_image(img, False)
    # im = Image.open("C:\\Users\\Agustin\\Desktop\\Tp2Algoritmos1\\000.png")
    # im.show()

main()