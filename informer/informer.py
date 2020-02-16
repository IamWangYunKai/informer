# -*- coding: utf-8 -*-
import socket
from informer.network import send_package, send_simple_package
from informer.utils import encode_img, encode_cmd, encode_debug_message, to_json
from informer import config

class Informer():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        self.cnt = 0
        self.message_dick = {'cnt':0}
        
    
    def send_vision(self, img, debug=False):
        data = encode_img(img)
        send_package(data, self.socket, config.ADDRESS, config.VISION_PORT, debug=debug)
    
    def send_cmd(self, v, w, c, debug=False):
        data = encode_cmd(v, w, c)
        send_simple_package(data, self.socket, config.ADDRESS, config.CMD_PORT, debug=debug)
        
    def draw_box(self, lt_x, lt_y, width, height, message='', color='red', **kwargs):
        data = to_json(dtype='box',
                                    lt_x=lt_x, lt_y=lt_y, width=width, height=height,
                                    message=message,
                                    color=color)
        self.message_dick[str(self.cnt)] = data
        self.cnt += 1
        self.message_dick['cnt'] = self.cnt
        #send_simple_package(data, self.socket, config.ADDRESS, config.DEBUG_PORT)
        
    def draw_center_box(self, ct_x, ct_y, width, height, message='', color='red'):
        data = encode_debug_message(dtype='center_box',
                                    ct_x=ct_x, ct_y=ct_y, width=width, height=height,
                                    message=message,
                                    color=color)
        send_simple_package(data, self.socket, config.ADDRESS, config.DEBUG_PORT)
        
    def draw_line(self, s_x, s_y, e_x, e_y, color='red'):
        data = encode_debug_message(dtype='line',
                                    s_x=s_x, s_y=s_y, e_x=e_x, e_y=e_y,
                                    color=color)
        send_simple_package(data, self.socket, config.ADDRESS, config.DEBUG_PORT)
        
    def clear(self):
        data = encode_debug_message(dtype='clear')
        send_simple_package(data, self.socket, config.ADDRESS, config.DEBUG_PORT)
        
    def draw(self):
        #print(self.message_dick)
        data = encode_debug_message(self.message_dick)
        #print(data)
        self.message_dick = {'cnt':0}
        self.cnt = 0
        #data = encode_debug_message(dtype='draw')
        #send_simple_package(data, self.socket, config.ADDRESS, config.DEBUG_PORT)