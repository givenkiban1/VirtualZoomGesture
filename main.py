import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np



def processPng(src):
    bgr = src[:, :, :3]  # Channels 0..2
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    # Some sort of processing...

    bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    alpha = src[:, :, 3]  # Channel 3
    return np.dstack([bgr, alpha])


# making use of camera source 0
cap = cv2.VideoCapture(0)

# not sure what 3 and 4 are ...
width = 1366
height = 720
cap.set(3, width)
cap.set(4, height)

#detection Confidence = 80%
detector = HandDetector(detectionCon=0.8)

startDistance = None
scale = 0
cx, cy = 200,200

while True:
    success, img = cap.read()

    hands, img = detector.findHands(img)

    if len(hands)==2:
        # print("Zoom hands detected")

        # print(detector.fingersUp(hands[0]), detector.fingersUp(hands[1]))

        if (detector.fingersUp(hands[0]) == detector.fingersUp(hands[1]) and detector.fingersUp(hands[1])==[1,1,0,0,0]):
            # print("Zoom Gesture")

            lmList1 = hands[0]["lmList"]
            lmList2 = hands[1]["lmList"]

            if (startDistance is None):
                # length, info, img = detector.findDistance(lmList1[8], lmList2[8], img)
                length, info, img = detector.findDistance(hands[0]["center"], hands[1]["center"], img)
                # print(length)
                startDistance = length

            # point 8 is the tip of index finger
            # length, info, img = detector.findDistance(lmList1[8], lmList2[8], img)

            # finding distance between center of hands ...
            length, info, img = detector.findDistance(hands[0]["center"], hands[1]["center"], img)
            scale = (length - startDistance)//2
            cx, cy = info[4:]

            print(scale)


    # Use Flip code 0 to flip vertically, 1 to flip horizontally
    img = cv2.flip(img, 1)

    #loading up my gintec solutions logo
    # img1 = cv2.imread("Gintec Small.png", cv2.IMREAD_UNCHANGED)
    img1 = cv2.imread("Gintec Small white.png")

    h1, w1, _= img1.shape
    print(h1, w1)

    newH, newW = int((h1 + scale)//2) * 2, int((w1 + scale)//2) * 2

    print(newH, newH)

    img1 = cv2.resize(img1, (newW, newH))

    # img1 = processPng(img1)

    print(cy - newH // 2, ":", cy + newH // 2)
    print(cx - newW // 2, ":", cx + newW // 2)
    try:
        img[cy-newH//2:cy+newH//2, cx-newW//2:cx+newW//2] = img1
    except:
        print("can't display image because it is out of bounds")
        pass
    cv2.imshow("Image", img)
    # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('image', width, height)

    cv2.waitKey(1)
