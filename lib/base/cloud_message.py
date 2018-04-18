#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import time

class CloudMessage(dict):
    def __init__(self, cid):
        self['ack'] = 0
        self['mid'] = str(int(time.time()))
        self['payload'] = {"code": 0, "operation": 0}
        self['to'] = cid
        self['type'] = 2
    @property
    def operation(self):
        return self['payload']['operation']

    @operation.setter
    def operation(self, operation):
        self['payload']['operation'] = operation

    @property
    def data(self):
        return  self['payload']['data']
    @data.setter
    def data(self, data):
        self['payload']['data'] = data

    @property
    def msg(self):
        return self['payload']['msg']

    @msg.setter
    def msg(self, msg):
        self['payload']['msg'] = msg

    @property
    def code(self):
        return self['payload']['code']

    @code.setter
    def code(self,code):
        self['payload']['code'] = code

