from informer import Informer
from time import sleep
import random

if __name__ == '__main__':
    ifm = Informer(random.randint(100000,999999), block=False)
    """
    while True:
        ifm.send_message('1')
        sleep(0.01)
    """
