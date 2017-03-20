#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from functools import wraps
from datetime import datetime

def cloud_timer(func):
    @wraps(func)
    def get_request_time(*args, **kwargs):
        start_time = datetime.now()
        func()
        end_time = datetime.now()
        return func(*args, **kwargs)
    return  get_request_time

class ActionTimer(object):
    __slots__ = ['action_name', 'start_time', 'end_time', 'seconds']
    def __init__(self, name, start_time, end_time):
        self.action_name = name
        self.start_time = start_time
        self.end_time = end_time
        self.seconds = self.__get_seconds__()

    def __get_seconds__(self):
        time_delta = self.end_time - self.start_time
        return  time_delta.total_seconds()

class ActionStatics(object):
    __slots__ = ['action_name', 'max_time', 'min_time', 'total_time', 'count']

    def __init__(self, name):
        self.action_name = name
        self.max_time = 0
        self.min_time = 0
        self.count = 0
        self.total_time = 0

    def add_action_timer(self, action_timer):
        if self.action_name != action_timer.name:
            return
        else:
            self.action_name = action_timer.name
        if self.min_time > action_timer.seconds:
            self.min_time = action_timer.seconds
        if self.max_time < action_timer.seconds:
            self.max_time = action_timer.seconds
        self.count += 1
        self.total_time += action_timer.seconds



class CloudTimer(object):
    def __init__(self):
        self.actions = []

    def add_action_timer(self, action_timer):
        if action_timer.action_name not in self.actions:
            self.actions.append(action_timer.action_name)
        self.__setattr__(action_timer.action_name, action_timer)

class TimerStatics(object):

    def __init__(self):
        self.times = []


    def add_cloud_timer(self, cloud_timer):
        self.times.append(cloud_timer)

    def format_output(self, keys):
        output = ""
        for i in range(len(keys)):
            output += "{0[%s]:<15}" %(i)
        return output

    def print_statics(self, actions=None):
        string = self.format_output(actions)
        print string.format(actions)
        for tmp_time in self.times:
            data = []
            for action in actions:
                if hasattr(tmp_time, action):
                    action_time = getattr(tmp_time, action)
                    data.append(action_time.seconds)
                else:
                    data.append("-")
            string = self.format_output(data)
            print string.format(data)


if __name__ == "__main__":
    import time
    from clouduser import CloudUser
    instances = []
    cloud_statics = TimerStatics()
    for i in range(20):
        clouduser01 = CloudUser('cpd12521277'+str(i), '029694a0fafac97c5435a1a97a909222', "9599e53c")
        inst = clouduser01.start_instance("com.netease.stzb.haima")
        instances.append(inst)

    time.sleep(10)
    for inst in instances:
        inst.stop_instance()
        cloud_statics.add_cloud_timer(inst.cloud_timer)

    cloud_statics.print_statics(['registry_sdk', 'get_config', 'get_cid', 'get_instance', 'all_request', 'got_instance', 'get_input','stop_instance'])




