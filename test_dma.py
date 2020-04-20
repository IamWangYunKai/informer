from informer import Informer
from time import sleep
import random

if __name__ == '__main__':
    ifm = Informer(random.randint(100000,999999))
    ifm.send_sim_goal(random.randint(-500, 500)/100.0, random.randint(-500, 500)/100.0)
    while True:
        data = ifm.get_sim_info()
        if data != None:
            x, y = data['x'], data['y']
        sleep(0.01)