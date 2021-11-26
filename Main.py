import cv2
import numpy as np

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
cap = cv2.VideoCapture(0)
# i = 0
while cv2.waitKey(1) == -1:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # detecting the faces
    faces = faceCascade.detectMultiScale(grayFrame, 1.1, 4)
    for (x, y, w, h) in faces:
        # puts a retangle on the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # cv2.imwrite('Face' + str(i) + '.jpg', frame)
        # i+=1
    # detecting the eyes
    eyes = eyeCascade.detectMultiScale(grayFrame, 1.1, 4)
    for (xe, ye, we, he) in eyes:
        # puts a retangle on the eyes
        cv2.rectangle(frame, (xe, ye), (xe + we, ye + he), (0, 255, 0), 2)
    cv2.imshow('video original', frame)
