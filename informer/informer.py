# -*- coding: utf-8 -*-
import json
import socket
import threading
from time import sleep
from informer.network import send_package, send_simple_package
import informer.utils as utils
from informer import config

class Informer():
    def __init__(self, robot_id=None, block=True):
        self.robot_id = str(robot_id)
        self.block = block
        self.register_keys = config.REGISTER_KEYS
        self.port_dict = config.PORT_DICT
        self.socket_dict = {}
        self.data_dict = {}
        self.connect_state = {}
        for key in self.register_keys:
            self.socket_dict[key] = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            if self.robot_id == None:
                self.data_dict[key] = ('server:'+key).encode("utf-8")
            else:
                data = {'Mtype':'register', 'Pri':5, 'Id':self.robot_id, 'Data':'message'}
                self.data_dict[key] = json.dumps(data).encode()
            self.socket_dict[key].sendto(self.data_dict[key], (config.PUBLICT_IP, self.port_dict[key]))
            
        for key in self.register_keys:
            recv_thread = threading.Thread(
                    target=self.connect, args=(key, self.socket_dict[key])
                    )
            recv_thread.start()
            
        # wait for sending packages
        if self.block:
            while set(self.register_keys) != set(self.connect_state.keys()):
                sleep(0.001)
        print('start to work...')
        
        if 'clock' in self.register_keys:
            self.cloc_sync_thread = threading.Thread(
                target=self.cloc_sync, args=()
            )
            self.cloc_sync_thread.start()
            
        if 'cmd' in self.register_keys:
            self.cmd_recv_thread = threading.Thread(
                target=self.cmd_recv, args=()
            )
            self.cmd_recv_thread.start()
  
        if 'message' in self.register_keys:
            self.message_recv_thread = threading.Thread(
                target=self.message_recv, args=()
            )
            self.message_recv_thread.start()
            
        if 'sim' in self.register_keys:
            self.sim_recv_thread = threading.Thread(
                target=self.sim_recv, args=()
            )
            self.sim_recv_thread.start()

        # debug info
        self.cnt = 0
        self.debug_dict = {}
        
    def connect(self, key, sock):
        data = ''
        while len(data) < 1:
        	data, address = sock.recvfrom(65535)
        data = str(data, encoding = "utf-8")
        try:
            ip = data.split(':')[0]
            port = int(data.split(':')[1])
            print('Get IP/port', ip, ':', port, 'as', key)
            self.connect_state[key] = True
        except:
            print('Error when connect', key, '.\tGet', data)
    
    def send_vision(self, img, isGrey=False, timestamp=None, debug=False):
        data = utils.encode_img(img, isGrey)
        send_package(data, self.socket_dict['vision'], config.PUBLICT_IP, self.port_dict['vision'], debug=debug, timestamp=timestamp)
    
    def send_sensor_data(self, v, w, c, debug=False):
        data = utils.encode_sensor(v, w, c)
        send_simple_package(data, self.socket_dict['sensor'], config.PUBLICT_IP, self.port_dict['sensor'], debug=debug)
        
    def draw_box(self, lt_x, lt_y, width, height, message='', color='red', **kwargs):
        data = utils.to_json(dtype='box',
                       lt_x=lt_x, lt_y=lt_y, width=width, height=height,
                       message=message,
                       color=color)
        self.debug_dict[str(self.cnt)] = data
        self.cnt += 1
        
    def draw_center_box(self, ct_x, ct_y, width, height, message='', color='red'):
        data = utils.to_json(dtype='center_box',
                       ct_x=ct_x, ct_y=ct_y, width=width, height=height,
                       message=message,
                       color=color)
        self.debug_dict[str(self.cnt)] = data
        self.cnt += 1
        
    def draw_line(self, s_x, s_y, e_x, e_y, color='red'):
        data = utils.to_json(dtype='line',
                       s_x=s_x, s_y=s_y, e_x=e_x, e_y=e_y,
                       color=color)
        self.debug_dict[str(self.cnt)] = data
        self.cnt += 1
        
    def clear(self):
        data = utils.to_json(dtype='clear')
        self.debug_dict[str(self.cnt)] = data
        self.cnt += 1
        
    def draw(self):
        data = utils.encode_debug_message(self.debug_dict)
        self.debug_dict = {}
        self.cnt = 0
        send_simple_package(data, self.socket_dict['debug'], config.PUBLICT_IP, self.port_dict['debug'])
        
    def cloc_sync(self):
        while True:
            data, addr = self.socket_dict['clock'].recvfrom(65535)
            new_data = bytes(str(int(data)-1), 'utf-8')
            send_package(new_data, self.socket_dict['clock'], config.PUBLICT_IP, self.port_dict['clock'])
            
    def cmd_recv(self):
        while True:
            data,addr = self.socket_dict['cmd'].recvfrom(65535)
            json_data = json.loads(data.decode('utf-8'))
            self.parse_cmd(json_data)
            
    def parse_cmd(self, cmd):
        pass
    
    def send_message(self, data, mtype='normal', pri=5, debug=False):
        data = utils.encode_message(data, self.robot_id, mtype, pri)
        send_simple_package(data, self.socket_dict['message'], config.PUBLICT_IP, self.port_dict['message'], debug=debug)
        
    def send_sim(self, v, w):
        data = {"v":v, "w":w}
        data = utils.encode_message(data, self.robot_id, mtype='cmd', pri=5)
        send_simple_package(data, self.socket_dict['sim'], config.PUBLICT_IP, self.port_dict['sim'])
        
    def message_recv(self):
        while True:
            data,addr = self.socket_dict['message'].recvfrom(65535)
            json_data = json.loads(data.decode('utf-8'))
            self.parse_message(json_data)
            
    def parse_message(self, message):
        message_type = message['Mtype']
        pri = message['Pri']
        robot_id = message['Id']
        data = message['Data']
        #print(message_type, pri, robot_id, data)
        
    def sim_recv(self):
        while True:
            data,addr = self.socket_dict['sim'].recvfrom(65535)
            json_data = json.loads(data.decode('utf-8'))
            self.parse_sim(json_data)
            
    def parse_sim(self, message):
        message_type = message['Mtype']
        pri = message['Pri']
        robot_id = message['Id']
        data = message['Data']
        #print(message_type, pri, robot_id, data)