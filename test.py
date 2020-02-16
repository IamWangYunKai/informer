from informer import Informer
from time import sleep
import random

if __name__ == '__main__':
    ifm = Informer()
    #ifm.draw_box(500, 300, 200, 80, "person", 'blue')
    #ifm.draw_center_box(500, 300, 200, 80, "person")
    #ifm.draw_line(0,0, 100, 100)
    while True:
        #ifm.clear()
        #sleep(0.01)
        if random.random() > 0.5 :
            ifm.draw_box(500, 300, 200, 80, "person", 'blue')
            ifm.draw_box(300, 400, 50, 50, "cat", 'red')
            #ifm.draw_center_box(300, 400, 100, 180, "person", 'blue')
        else:
            ifm.draw_box(300, 400, 50, 50, "cat", 'red')
        ifm.draw()
        sleep(0.5)