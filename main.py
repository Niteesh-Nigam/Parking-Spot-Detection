import cv2
import pickle
import cvzone
import numpy as np
import time

#Video feed
cap = cv2.VideoCapture('./parking_1920_1080.mp4')
width, height = 69,28

def load_positions():
    with open('CarParkPos', 'rb') as f:
        return pickle.load(f)

posList = load_positions()
last_time_checked = time.time()

def checkParkingSpace(imgPro):

    spaceCounter = 0


    for pos in posList:
        x,y = pos
        # cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height),(255,0,0))

        imgCrop = imgPro[y:y+height,x:x+width]
        # cv2.imshow(str(x*y),imgCrop)
        # cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height),(255,0,0))
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img,str(count),(x,y+height-10),scale=0.7,thickness=1, offset=0,colorR=(0,0,255))


        if count<380:
            color = (0,255,0)
            spaceCounter+=1
        else:
            color = (0,0,255)
        cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height),color,2)

    cvzone.putTextRect(img,f'Free Spaces{spaceCounter}/{len(posList)}',(100,50),scale=2,thickness=2, offset=20,colorR=(0,255,0))

while True:
    ret,img = cap.read()
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)

    if time.time() - last_time_checked > 5:  # Check if 5 seconds have passed
        posList = load_positions()  # Reload positions
        last_time_checked = time.time()  # Reset the timer

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(3,3),1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 19,17)

    imgMedian = cv2.medianBlur(imgThreshold,3)
    kernel = np.ones((3,3),np.uint8)
    imgDilate = cv2.dilate(imgMedian,kernel, iterations=1)
    # print(imgDilate.shape)
    


    checkParkingSpace(imgDilate)

    # for pos in posList:
        # cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height),color,2)



    cv2.imshow("image",img)
    # cv2.imshow("imageBlur", imgBlur)
    # cv2.imshow("imgThresh",imgThreshold)
    # cv2.imshow("medianBlur",imgDilate)

    cv2.waitKey(1)