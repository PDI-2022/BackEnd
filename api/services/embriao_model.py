import sys
import cv2
import traceback




def embriao_detect(embriao_model, frame):
    rets = []
    res = embriao_model(frame)

    for i in res.xyxy[0]:
        x1 = int(i[0])
        y1 = int(i[1])
        x2 = int(i[2])
        y2 = int(i[3])
        if i[5] == 4:
            [x1,y1,x2,y2] * 2
        rets.append([[x1,y1,x2,y2], i[4], int(i[5])])
    return rets

