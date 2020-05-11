# -*- coding: utf-8 -*-
import random
import numpy as np
from time import sleep
from informer import Informer, config
    
if __name__ == '__main__':
    # user settings
    ifm = Informer(random.randint(100000,999999), block=False)
    # get your data

    while True:
        # get image
        image = np.zeros([1280, 720, 3], np.uint8)
        # get robot command
        v = random.random()*5
        w = random.random()*10 - 5
        c = False if random.random() > 0.3 else True
        # get debug message
        for _ in range(random.randint(2, 5)):
            ifm.draw_box(random.randint(0, 1200), random.randint(0, 1200), random.randint(10, 200), random.randint(10, 200), random.sample(config.colors, 1)[0], random.sample(config.colors, 1)[0])
            ifm.draw_center_box(random.randint(100, 1100), random.randint(100, 1100), random.randint(10, 400), random.randint(10, 400), random.sample(config.colors, 1)[0], random.sample(config.colors, 1)[0])
        
        # send image
        ifm.send_vision(image, False)
        # send robot command
        ifm.send_sensor_data(v, w, c)
        # send debug message
        ifm.draw()
        #sleep(1/100.)