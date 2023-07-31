from keras.models import load_model
import numpy as np
import cv2
import mediapipe as mp
import math
from pathlib import Path
folder = Path(__file__).parent.resolve()

np.set_printoptions(suppress=True)
model = load_model(f"{folder}\\AI\\keras_model.h5", compile=False)
class_names = open(f"{folder}\\AI\\labels.txt", "r").readlines()


def angleCheck(myAngle, targetAngle, addOn=20):
    return targetAngle - addOn < myAngle < targetAngle + addOn


class PoseDetector:
    def __init__(self, mode=False, smooth=True,
                 detectionCon=0.3, trackCon=0.3):
        self.bboxInfo = None
        self.results = None
        self.lmList = None
        self.mode = mode
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(static_image_mode=self.mode,
                                     smooth_landmarks=self.smooth,
                                     min_detection_confidence=self.detectionCon,
                                     min_tracking_confidence=self.trackCon)

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True, bboxWithHands=False):
        self.lmList = []
        self.bboxInfo = {}

        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy, cz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                self.lmList.append([id, cx, cy, cz])

            # Ensure all required indexes exist before trying to access
            if len(self.lmList) > max(29, 18, 17, 14, 13, 1):
                ad = abs(self.lmList[12][1] - self.lmList[11][1]) // 2
                if bboxWithHands:
                    if self.lmList[18][1] < self.lmList[14][1] and self.lmList[18][1] < self.lmList[12][1]:
                        x1 = self.lmList[18][1] - ad
                    elif self.lmList[14][1] < self.lmList[18][1] and self.lmList[14][1] < self.lmList[12][1]:
                        x1 = self.lmList[14][1] - ad
                    else:
                        x1 = self.lmList[12][1] - ad

                    if self.lmList[17][1] > self.lmList[13][1] and self.lmList[17][1] > self.lmList[11][1]:
                        x2 = self.lmList[17][1] + ad
                    elif self.lmList[13][1] > self.lmList[17][1] and self.lmList[13][1] > self.lmList[11][1]:
                        x2 = self.lmList[13][1] + ad
                    else:
                        x2 = self.lmList[11][1] + ad
                else:
                    x1 = self.lmList[14][1] - ad
                    x2 = self.lmList[13][1] + ad

                y2 = self.lmList[29][2] + ad
                if self.lmList[15][2] < self.lmList[1][2]:
                    y1 = self.lmList[15][2] - ad
                elif self.lmList[16][2] < self.lmList[1][2]:
                    y1 = self.lmList[16][2] - ad
                else:
                    y1 = self.lmList[1][2] - ad

                bbox = (x1, y1, x2 - x1, y2 - y1)
                cx, cy = bbox[0] + (bbox[2] // 2), bbox[1] + bbox[3] // 2

                self.bboxInfo = {"bbox": bbox, "center": (cx, cy)}

                if draw:
                    cv2.rectangle(img, bbox, (255, 0, 255), 3)
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        return self.lmList, self.bboxInfo

    def findAngle(self, img, p1, p2, p3, draw=True):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angle

    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]


def draw_point(blank_img, lmList):
    x_0, y_0 = lmList[0][1], lmList[0][2]
    x_1, y_1 = lmList[1][1], lmList[1][2]
    x_2, y_2 = lmList[2][1], lmList[2][2]
    x_3, y_3 = lmList[3][1], lmList[3][2]
    x_4, y_4 = lmList[4][1], lmList[4][2]
    x_5, y_5 = lmList[5][1], lmList[5][2]
    x_6, y_6 = lmList[6][1], lmList[6][2]
    x_7, y_7 = lmList[7][1], lmList[7][2]
    x_8, y_8 = lmList[8][1], lmList[8][2]
    x_9, y_9 = lmList[9][1], lmList[9][2]
    x_10, y_10 = lmList[10][1], lmList[10][2]
    x_11, y_11 = lmList[11][1], lmList[11][2]
    x_12, y_12 = lmList[12][1], lmList[12][2]
    x_13, y_13 = lmList[13][1], lmList[13][2]
    x_14, y_14 = lmList[14][1], lmList[14][2]
    x_15, y_15 = lmList[15][1], lmList[15][2]
    x_16, y_16 = lmList[16][1], lmList[16][2]
    x_17, y_17 = lmList[17][1], lmList[17][2]
    x_18, y_18 = lmList[18][1], lmList[18][2]
    x_19, y_19 = lmList[19][1], lmList[19][2]
    x_20, y_20 = lmList[20][1], lmList[20][2]
    x_21, y_21 = lmList[21][1], lmList[21][2]
    x_22, y_22 = lmList[22][1], lmList[22][2]
    x_23, y_23 = lmList[23][1], lmList[23][2]
    x_24, y_24 = lmList[24][1], lmList[24][2]
    x_25, y_25 = lmList[25][1], lmList[25][2]
    x_26, y_26 = lmList[26][1], lmList[26][2]
    x_27, y_27 = lmList[27][1], lmList[27][2]
    x_28, y_28 = lmList[28][1], lmList[28][2]
    x_29, y_29 = lmList[29][1], lmList[29][2]
    x_30, y_30 = lmList[30][1], lmList[30][2]
    x_31, y_31 = lmList[31][1], lmList[31][2]
    x_32, y_32 = lmList[32][1], lmList[32][2]

    cv2.line(blank_img, (x_11, y_11), (x_12, y_12), (255, 255, 255), 2)
    cv2.line(blank_img, (x_13, y_13), (x_11, y_11), (255, 255, 255), 2)
    cv2.line(blank_img, (x_12, y_12), (x_14, y_14), (255, 255, 255), 2)
    cv2.line(blank_img, (x_16, y_16), (x_14, y_14), (255, 255, 255), 2)
    cv2.line(blank_img, (x_13, y_13), (x_15, y_15), (255, 255, 255), 2)
    cv2.line(blank_img, (x_16, y_16), (x_20, y_20), (255, 255, 255), 2)
    cv2.line(blank_img, (x_18, y_18), (x_20, y_20), (255, 255, 255), 2)
    cv2.line(blank_img, (x_16, y_16), (x_18, y_18), (255, 255, 255), 2)
    cv2.line(blank_img, (x_16, y_16), (x_22, y_22), (255, 255, 255), 2)
    cv2.line(blank_img, (x_12, y_12), (x_24, y_24), (255, 255, 255), 2)
    cv2.line(blank_img, (x_11, y_11), (x_23, y_23), (255, 255, 255), 2)
    cv2.line(blank_img, (x_23, y_23), (x_24, y_24), (255, 255, 255), 2)
    cv2.line(blank_img, (x_23, y_23), (x_25, y_25), (255, 255, 255), 2)
    cv2.line(blank_img, (x_24, y_24), (x_26, y_26), (255, 255, 255), 2)
    cv2.line(blank_img, (x_15, y_15), (x_21, y_21), (255, 255, 255), 2)
    cv2.line(blank_img, (x_15, y_15), (x_19, y_19), (255, 255, 255), 2)
    cv2.line(blank_img, (x_15, y_15), (x_17, y_17), (255, 255, 255), 2)
    cv2.line(blank_img, (x_17, y_17), (x_19, y_19), (255, 255, 255), 2)
    cv2.line(blank_img, (x_9, y_9), (x_10, y_10), (255, 255, 255), 2)
    cv2.line(blank_img, (x_0, y_0), (x_4, y_4), (255, 255, 255), 2)
    cv2.line(blank_img, (x_5, y_5), (x_4, y_4), (255, 255, 255), 2)
    cv2.line(blank_img, (x_5, y_5), (x_6, y_6), (255, 255, 255), 2)
    cv2.line(blank_img, (x_6, y_6), (x_8, y_8), (255, 255, 255), 2)
    cv2.line(blank_img, (x_0, y_0), (x_1, y_1), (255, 255, 255), 2)
    cv2.line(blank_img, (x_1, y_1), (x_2, y_2), (255, 255, 255), 2)
    cv2.line(blank_img, (x_2, y_2), (x_3, y_3), (255, 255, 255), 2)
    cv2.line(blank_img, (x_3, y_3), (x_7, y_7), (255, 255, 255), 2)
    cv2.line(blank_img, (x_26, y_26), (x_28, y_28), (255, 255, 255), 2)
    cv2.line(blank_img, (x_25, y_25), (x_27, y_27), (255, 255, 255), 2)
    cv2.line(blank_img, (x_32, y_32), (x_28, y_28), (255, 255, 255), 2)
    cv2.line(blank_img, (x_31, y_31), (x_27, y_27), (255, 255, 255), 2)
    cv2.line(blank_img, (x_32, y_32), (x_30, y_30), (255, 255, 255), 2)
    cv2.line(blank_img, (x_31, y_31), (x_29, y_29), (255, 255, 255), 2)
    cv2.line(blank_img, (x_28, y_28), (x_30, y_30), (255, 255, 255), 2)
    cv2.line(blank_img, (x_27, y_27), (x_29, y_29), (255, 255, 255), 2)

    for landmark in lmList:
        cv2.circle(blank_img, (landmark[1], landmark[2]), 4, (0, 0, 255), cv2.FILLED)
        cv2.circle(blank_img, (landmark[1], landmark[2]), 4, (255, 255, 255), 1)


def model_AI(blank_img):
    blank_img = np.asarray(blank_img, dtype=np.float32).reshape(1, 224, 224, 3)
    blank_img = (blank_img / 127.5) - 1

    prediction = model.predict(blank_img)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    print("Class:", class_name[2:], end="")
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

    return class_name[2:]
