# -*- coding: utf-8 -*-
import cv2
import random
from informer import Informer

if __name__ == '__main__':
    ifm = Informer()
    cam = cv2.VideoCapture(0)
    cam.set(3,1920)
    while True:
        if cam.isOpened(): 
            success,image=cam.read()
            ifm.send_vision(image)
            
            v = random.random()*5
            w = random.random()*10 - 5
            c = False if random.random() > 0.3 else True
            ifm.send_cmd(v, w, c)

        else:
            cam.release()
            print("Service Exit !!!")