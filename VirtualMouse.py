import cv2
import numpy as np
import HandTrackingModule as htm
import time
import mouse
import autopy.mouse
from playsound import playsound
import os
import tkinter as tk
from tkinter import Button, Label
base_dir = os.path.dirname(__file__)
file_path_left = os.path.join(base_dir, './focus_change_keyboard.caf')
file_path_right = os.path.join(base_dir, './focus_change_small.caf')


##########################
wCam, hCam = 1920, 1080
frameR = 380  # Frame Reduction
smoothening = 7
#########################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0


cap = cv2.VideoCapture(1)


cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()


# print(wScr, hScr)

while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1, y1, x2, y2)

    # 3. Check which fingers are up
    fingers = detector.fingersUp()
    # print(fingers)
    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                  (255, 0, 255), 2)


    #Only Thumb Finger : Moving Mode
    if len(fingers) >= 3 and fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
        # 5. Convert Coordinates
        x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
        y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

        # 6. Smoothen Values
        clocX = plocX + (x3 - plocX) / smoothening
        clocY = plocY + (y3 - plocY) / smoothening

        # 7. Move Mouse
        autopy.mouse.move(wScr - clocX, clocY)
        cv2.circle(img, (x1, y1), 15, (0, 128, 255), cv2.FILLED)
        plocX, plocY = clocX, clocY



    # Both Thumb and index fingers are up : Left Clicking Mode
    if len(fingers) >= 3 and fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
        # 9. Find distance between fingers
        length, img, lineInfo = detector.findDistance(4, 8, img)  # Use thumb (4) and index (8) fingers
        # 10. Click mouse if distance short

        if length < 45:
            cv2.circle(img, (lineInfo[2], lineInfo[1]),
                       7, (0, 255, 0), cv2.FILLED)
            playsound(file_path_left)
            #print("Left Clicked")
            autopy.mouse.click()


    # Right click when middle and index close
    if len(fingers) >= 3 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
        # 9. Find distance between fingers
        length, img, lineInfo = detector.findDistance(8, 12, img)  # Use index (8) and middle (12) fingers
        # 10. Click mouse if distance short

        if length < 50:
            cv2.circle(img, (lineInfo[2], lineInfo[1]),
                       7, (0, 255, 0), cv2.FILLED)
            playsound(file_path_right)
            #print("Right Clicked")
            mouse.click(button="right")



    if len(fingers) >= 3 and fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
        mouse.wheel(delta=3)
    elif len(fingers) >= 3 and fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
        mouse.wheel(delta=-3)



    # 11. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    #cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
    #            (255, 0, 0), 3)
    # 12. Display

    #cv2.imshow("Image", img)
    #cv2.waitKey(1)