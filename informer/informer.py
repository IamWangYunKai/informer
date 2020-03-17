# -*- coding: utf-8 -*-
import json
import socket
import threading
from time import sleep
from informer.network import send_package, send_simple_package
from informer.utils import encode_img, encode_cmd, encode_debug_message, to_json
from informer import config

class Informer():
    def __init__(self):
        self.register_key = ['clock', 'cmd', 'vision', 'sensor', 'debug']
        self.socket_dict = {}
        self.data_dict = {}
        self.port_dict = {}
        self.client_ip = ''
        for key in self.register_key:
            self.socket_dict[key] = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            self.data_dict[key] = ('server:'+key).encode("utf-8")
            self.socket_dict[key].sendto(self.data_dict[key], config.PUBLICT_ADDRESS)
            
        for key in self.register_key:
            rec_thread = threading.Thread(
                    target=self.connect, args=(key, self.socket_dict[key])
                    )
            rec_thread.start()
            
        self.cloc_sync_thread = threading.Thread(
            target=self.cloc_sync, args=()
        )
        
        self.cmd_rec_thread = threading.Thread(
            target=self.cmd_rec, args=()
        )
        
        self.cnt = 0
        self.message_dick = {}
        
        while set(self.register_key) != set(self.port_dict.keys()):
            sleep(0.001)
        print('start to work...\n', self.client_ip, self.port_dict)
        
        # automaticly start cloc synchronization thread
        self.cloc_sync_thread.start()
        self.cmd_rec_thread.start()
        
    def connect(self, key, sock):
        data = ''
        while len(data) < 1:
        	data, address = sock.recvfrom(1024)
        data = str(data, encoding = "utf-8")
        ip = data.split(':')[0]
        port = int(data.split(':')[1])
        print('Get IP/port', ip, ':', port, 'as', key)
        self.client_ip = ip
        self.port_dict[key] = port
    
    def send_vision(self, img, isGrey=False, timestamp=None, debug=False):
        data = encode_img(img, isGrey)
        send_package(data, self.socket_dict['vision'], self.client_ip, self.port_dict['vision'], debug=debug, timestamp=timestamp)
    
    def send_cmd(self, v, w, c, debug=False):
        data = encode_cmd(v, w, c)
        send_simple_package(data, self.socket_dict['sensor'], self.client_ip, self.port_dict['sensor'], debug=debug)
        
    def draw_box(self, lt_x, lt_y, width, height, message='', color='red', **kwargs):
        data = to_json(dtype='box',
                       lt_x=lt_x, lt_y=lt_y, width=width, height=height,
                       message=message,
                       color=color)
        self.message_dick[str(self.cnt)] = data
        self.cnt += 1
        
    def draw_center_box(self, ct_x, ct_y, width, height, message='', color='red'):
        data = to_json(dtype='center_box',
                       ct_x=ct_x, ct_y=ct_y, width=width, height=height,
                       message=message,
                       color=color)
        self.message_dick[str(self.cnt)] = data
        self.cnt += 1
        
    def draw_line(self, s_x, s_y, e_x, e_y, color='red'):
        data = to_json(dtype='line',
                       s_x=s_x, s_y=s_y, e_x=e_x, e_y=e_y,
                       color=color)
        self.message_dick[str(self.cnt)] = data
        self.cnt += 1
        
    def clear(self):
        data = to_json(dtype='clear')
        self.message_dick[str(self.cnt)] = data
        self.cnt += 1
        
    def draw(self):
        data = encode_debug_message(self.message_dick)
        self.message_dick = {}
        self.cnt = 0
        send_simple_package(data, self.socket_dict['debug'], self.client_ip, self.port_dict['debug'])
        
    def cloc_sync(self):
        while True:
            data, addr = self.socket_dict['clock'].recvfrom(65535)
            new_data = bytes(str(int(data)-1), 'utf-8')
            send_package(new_data, self.socket_dict['clock'], self.client_ip, self.port_dict['clock'])
            
    def cmd_rec(self):
        while True:
            data,addr = self.socket_dict['cmd'].recvfrom(65535)
            json_data = json.loads(data.decode('utf-8'))
            self.parse_cmd(json_data)
            
    def parse_cmd(self, cmd):
        pass