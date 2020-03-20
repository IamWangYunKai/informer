# -*- coding: utf-8 -*-
import cv2
import json

def encode_img(img, isGrey=False):
    if isGrey:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (img.shape[1],img.shape[0]), interpolation=cv2.INTER_AREA)
    ret, jpeg=cv2.imencode('.jpg', img)
    data = jpeg.tobytes()
    return data

def encode_sensor(v, w, c):
    data = {'v':v, 'w':w, 'c':c}
    data = json.dumps(data).encode()
    return data

def to_json(**kwargs):
    return json.dumps(kwargs)
    
def encode_debug_message(messages):
    data = json.dumps(messages).encode()
    return data