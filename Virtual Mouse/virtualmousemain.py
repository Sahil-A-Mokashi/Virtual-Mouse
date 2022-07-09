from aifc import Error

import cv2
import numpy as np
import pyautogui
from pyautogui import RIGHT

import HandTrackingModule as htm
import time
import autopy

##########################
wCam, hCam = 640, 480
frameR = 100  # Frame Reduction
smoothening = 7
#########################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
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
        x1, y1 = lmList [8][1:]
        x2, y2 = lmList [12][1:]
        # print(x1, y1, x2, y2)

    # 3. Check which fingers are up
    fingers = detector.fingersUp()
    # print(fingers)
    # cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
    #               (255, 0, 255), 2)

    if fingers[0] == 1 and fingers[1] == 1 and fingers[4] == 1:  # and fingers[2] == 1:
        length, img, lineInfo = detector.findDistance(4, 8, img)

        print(length)
        # 10. Click mouse if distance short
        if length > 20:  # and length1 < 10:
            # cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
            # autopy.mouse.click()
            pyautogui.scroll(200)
            # 11. Frame Rate
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 0, 0), 3)
    # 4. Only Index Finger : Moving Mode

    if fingers [1] == 1 and fingers[2] == 0:
        # 5. Convert Coordinates
        x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
        y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
        # 6. Smoothen Values
        clocX = plocX + (x3 - plocX) / smoothening
        clocY = plocY + (y3 - plocY) / smoothening

        # 7. Move Mouse
        try:
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
        except Error:
            cv2.putText(img, "Out of Bounds", (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 0, 0), 3)

    # 8. Both Index and middle fingers are up : Clicking Mode
    if fingers [1] == 1 and fingers[2] == 1:
        # 9. Find distance between fingers
        length, img, lineInfo = detector.findDistance(8, 12, img)
        print(length)
        # 10. Click mouse if distance short
        if length < 50:
            cv2.circle(img, (lineInfo [4], lineInfo[5]),
                             15, (0, 255, 0), cv2.FILLED)
            autopy.mouse.click()

            # 11. Frame Rate
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 0, 0), 3)


        if fingers[2] == 1 and fingers[1] == 1 and fingers[0] == 1:# and fingers[2] == 1:
            length, img, lineInfo = detector.findDistance(4, 12, img)

            print(length)
            # 10. Click mouse if distance short
            if length < 1000:  # and length1 < 10:
                #cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                # autopy.mouse.click()
                pyautogui.scroll(-200)
                # 11. Frame Rate
                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime
                cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 0, 0), 3)


        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 :
            length, img, lineInfo = detector.findDistance(8, 12, img)
            length1, img, lineInfo2 = detector.findDistance(12, 16, img)
            #length2, img, lineInfo3 = detector.findDistance(16, 20, img)

            print(length)
            # 10. Click mouse if distance short
            if length < 40 and length1 < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                #autopy.mouse.click()
                pyautogui.click(button='right')
                # 11. Frame Rate
                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime
                cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                            (255, 0, 0), 3)

        '''if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1 and fingers[0]==1:
            length0, img, lineInfo = detector.findDistance(4, 12, img)
            length, img, lineInfo = detector.findDistance(4, 20, img)
            length1, img, lineInfo2 = detector.findDistance(12, 20, img)
            if length < 40 and length1 < 40 and length0 < 40:
                x, y = pyautogui.position()
                pyautogui.dragTo(x, y, button='left')

                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime
                cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                            (255, 0, 0), 3)'''

    #cv2.waitKey(1)
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord('q'):
        break
    cv2.flip(img,1,img)
    cv2.imshow("Image", img)
cv2.destroyAllWindows()
