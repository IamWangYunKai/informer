# -*- coding: utf-8 -*-
import random
from time import sleep
from informer import Informer, config

config.PORT_DICT = {'message':10006,}
config.REGISTER_KEYS = list(config.PORT_DICT.keys())

class Talker(Informer):
    def parse_message(self, message):
        message_type = message['Mtype']
        pri = message['Pri']
        robot_id = message['Id']
        data = message['Data']
        print(message_type, pri, robot_id, data)
        
if __name__ == '__main__':
    ifm = Talker(robot_id=random.randint(100000,999999), block=True)
    
    while True:
        ifm.send_message(
                data="This is a test message",
                mtype='normal',
                pri=5)
        sleep(0.5)