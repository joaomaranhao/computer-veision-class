from HandTrackingModule import HandDetector, cv2, time
import os
import numpy as np

folderPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')
imagesList = os.listdir(folderPath)
overlayList = []
for imPath in imagesList:
    image = cv2.imread(os.path.join(folderPath, imPath))
    overlayList.append(image)


menu = overlayList[0]
drawColor = (255, 0, 255)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionConf=0.85)

while True:
    # Import image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Find Hand Ladmarks
    img = detector.findHands(img, draw=False)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # Check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)
        # If Selection mode (two fingers are up) we have to select
        if fingers[1] and fingers[2]:
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25),
                          drawColor, cv2.FILLED)
            if y1 < 129:
                if 204 < x1 < 353:
                    drawColor = (83, 83, 255)
                elif 371 < x1 < 520:
                    drawColor = (101, 209, 59)
                elif 538 < x1 < 687:
                    drawColor = (255, 162, 62)
                elif 705 < x1 < 854:
                    drawColor = (0, 255, 250)
                elif 872 < x1 < 1021:
                    drawColor = (244, 75, 241)
                elif 1099 < x1 < 1248:
                    drawColor = (0, 0, 0)

        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)

    # If Drawing Mode (index finger is up)

    # Setting menu image
    img[0:129, 0:1280] = menu
    cv2.imshow("image", img)
    cv2.waitKey(1)
