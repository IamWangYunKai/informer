# -*- coding: utf-8 -*-

MAX_LENGTH = 65535 - 16*4

PUBLICT_IP = '47.100.46.11'

PORT_DICT = {
        'vision':10001,
        'sensor':10002,
        'cmd':10003,
        'debug':10004,
        'clock':10005,
        }

REGISTER_KEYS = list(PORT_DICT.keys())

colors = ['black','white','darkGray','gray','lightGray','red','green','blue','cyan','magenta','yellow','darkRed','darkGreen','darkBlue','darkCyan','darkMagenta','darkYellow']