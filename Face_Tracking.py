import cv2
import numpy as np

a, b = 360, 240
fbRange = [6200,6800]
pid = [0.4,0.4,0]
pError = 0

# summons face detection code by Violet Jones
def findFace(img):
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)

    myFaceListC = []
    myFaceListArea = []

# determines areaface of face detection and the centre of the face
    for(x,y,a,b) in faces:
        cv2.rectangle(img, (x, y), (x + a, y + b), (0, 0, 255), 2)
        cx = x + a // 2
        cy = y + b // 2
        areaface = a * b
        cv2.circle(img,(cx,cy), 5,(255,0,0), cv2.FILLED)
        myFaceListC.append([cx, cy])
        myFaceListArea.append(areaface)
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0,0],0]

# determines whether drone is too close to target or not and corrects
def trackFace(info, a, pid, pError):
    areaface = info[1]
    x, y = info[0]
    fb = 0
    error = x-a//2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))

    if areaface > fbRange[0] and areaface < fbRange[1]:
        fb = 0
    elif areaface > fbRange[1]:
        fb = -20
    elif areaface < fbRange[0] and areaface != 0:
        fb = 20

    if x == 0:
        speed = 0
        error = 0

    print(speed, fb)

# any reference to "me" refers to the flight controller
    #me.send_rc_control(0,fb,0,speed)
    return error

cap = cv2.VideoCapture(0)
while True:
    _, img = cap.read()
    img = cv2.resize(img,(a,b))
    img, info = findFace(img)
    pError = trackFace(info, a, pid, pError)
    #print("Center", info[0],"Area", info[1])
    cv2.imshow("Output", img)
    cv2.waitKey(1)
