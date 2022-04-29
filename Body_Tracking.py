import cv2
import numpy as np

w, h = 800, 600
fbRange = [6200, 6800]
pid = [0.4, 0.4, 0]
pError = 0


# summons face detection code by Violet Jones
def findBody(img):
    bodyCascade = cv2.CascadeClassifier("haarcascade_fullbody.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bodies = bodyCascade.detectMultiScale(imgGray, 1.2, 8)

    myBodyListC = []
    myBodyListArea = []

    # determines area of face detection and the centre of the face
    for (x, y, w, h) in bodies:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        myBodyListC.append([cx, cy])
        myBodyListArea.append(area)
    if len(myBodyListArea) != 0:
        i = myBodyListArea.index(max(myBodyListArea))
        return img, [myBodyListC[i], myBodyListArea[i]]
    else:
        return img, [[0, 0], 0]


# determines whether drone is too close to target or not and corrects
def trackBody(info, w, pid, pError):
    area = info[1]
    x, y = info[0]
    fb = 0
    error = x - w // 2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))

    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -20
    elif area < fbRange[0] and area != 0:
        fb = 20

    if x == 0:
        speed = 0
        error = 0

    print(speed, fb)

    # any reference to "me" refers to the flight controller
    # me.send_rc_control(0,fb,0,speed)
    return error

cap = cv2. VideoCapture('slowclimb.mp4')
while True:
    _, img = cap.read()
    img = cv2.resize(img,(w,h))
    img, info = findBody(img)
    pError = trackBody(info, w, pid, pError)
    #print("Center", info[0],"Area", info[1])
    cv2.imshow("Output", img)
    cv2.waitKey(1)
