from informer import Informer, config
from time import sleep
import random

if __name__ == '__main__':
    ifm = Informer()
    while True:
        for _ in range(random.randint(50, 150)):
            ifm.draw_box(random.randint(0, 1200), random.randint(0, 1200), random.randint(10, 200), random.randint(10, 200), random.sample(config.colors, 1)[0], random.sample(config.colors, 1)[0])
            ifm.draw_center_box(random.randint(0, 1200), random.randint(0, 1200), random.randint(100, 400), random.randint(10, 200), random.sample(config.colors, 1)[0], random.sample(config.colors, 1)[0])
            ifm.draw_line(random.randint(0, 1200), random.randint(0, 1200), random.randint(0, 1200), random.randint(0, 1200), random.sample(config.colors, 1)[0])
        ifm.draw()
        #sleep(0.1)