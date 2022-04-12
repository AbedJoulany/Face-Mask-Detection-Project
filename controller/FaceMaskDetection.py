# import the necessary packages
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import imutils
import cv2
import math

from typing_extensions import runtime

from controller.simple_facerec import SimpleFacerec
from concurrent.futures import ThreadPoolExecutor
from controller.simple_facerec import SimpleFacerec
import threading

prototxtPath = r"face_detector\deploy.prototxt"
weightsPath = r"face_detector\res10_300x300_ssd_iter_140000.caffemodel"
maskNet = load_model("./controller/mask_detector.model")
FacesImagesFolder = r"savedImages/Faces"
FullImagesFolder = r"savedImages/FullImages"
pool = ThreadPoolExecutor(max_workers=1)

sfr = SimpleFacerec()
sfr.load_encoding_images("controller/images")

counter = 0


# known = RecognitionThread()


def known_faces(frame):
    face_locations, face_names = sfr.detect_known_faces(frame)
    for face_loc, name in zip(face_locations, face_names):
        # y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        # cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
        facesfilename = FacesImagesFolder + "/image_" + name + ".jpg"
        cv2.imwrite(facesfilename, frame)


def detect_and_predict_mask(frame, faceNet, maskNet):
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
                                 (104.0, 117.0, 123.0))

    faceNet.setInput(blob)
    detections = faceNet.forward()

    faces = []
    locs = []
    preds = []

    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

            face = frame[startY:endY, startX:endX]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)

            faces.append(face)
            locs.append((startX, startY, endX, endY))

    if len(faces) > 0:
        faces = np.array(faces, dtype="float32")
        preds = maskNet.predict(faces, batch_size=11)

    return (locs, preds)


def getFrame(frame, frameId, q, threadLock):
    faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
    global counter
    counter += 1
    frame = imutils.resize(frame, width=400)
    frame = cv2.flip(frame, 1)
    (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

    for (box, pred) in zip(locs, preds):
        (startX, startY, endX, endY) = box
        (mask, withoutMask) = pred

        # x = threading.Thread(target=known_faces(frame[startY:endY, startX:endX]))
        # x.daemon = True

        label = "No Mask" if mask > withoutMask else "Mask"
        color = (0, 0, 255) if label == "No Mask" else (0, 255, 0)

        # if (label == "No Mask") & (frameId % math.floor(30) == 0):
        # f = frame[startY:endY, startX:endX]
        if label == "No Mask" and counter % 15 == 0:
            # making a thread for face recognition
            pool.submit(run_rec, frame[startY:endY, startX:endX], q, threadLock)
            # thread_func(frame[startY:endY, startX:endX], q, threadLock)
            # fullimagesfilename = FullImagesFolder + "/image_" + str(int(frameId)) + ".jpg"
            # cv2.imwrite(fullimagesfilename, frame)

        label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

        cv2.putText(frame, label, (startX, startY - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
        cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

    return frame


def run_rec(frame, q, thread_lock):
    face_names = sfr.detect_known_faces(frame)
    for name in zip(face_names):
        # y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        # cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
        # faces_file_name = FacesImagesFolder + "/image_" + str(name) + ".jpg"
        # cv2.imwrite(faces_file_name, frame)
        try:
            thread_lock.acquire()
            q.put(frame)
            thread_lock.release()
        except:
            print("thread error")