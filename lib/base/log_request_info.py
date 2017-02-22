#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time
import random


class LogDevice():
    def __init__(self, sdk_type):
        self.sdk_type = sdk_type

    def get_str(self):
        return "---------"

class LogRequest():
    def __init__(self, sdk_type):
        self.device = LogDevice(sdk_type)
        self.sdk_type = sdk_type
        self.did = 123
        self.cid = 123123
        self.uid = "123123"
        self.pkg_name = "12312.12.123"
        self.access_key = "asdf3e"
        self.play_time = 123123
        self.wait_time = 123123
        self.chanel = 1231
        self.serial = '1231'
        self.app_id = "123123"


    def server_str(self, event_id, event_data=""):
        time_int = time.time()
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_int))
        date_int = int(time_int*1000)
        extra_id = "%s,%s,%s,%s" %(self.serial, self.did, self.app_id, self.chanel)
        return "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
            date, date_int, self.did, self.cid, self.pkg_name, self.uid, self.sdk_type, event_data, event_id,
            extra_id, self.access_key)



    def server_str_without_keys(self, event_id, keys, event_data=""):
        backup = {}
        for key in keys:
            if hasattr(self, key):
                backup[key] = getattr(self, key)
                setattr(self, key, "")
        output = self.server_str(event_id, event_data)
        for key, value in backup.items():
            setattr(self, key, value)
        return output

    def sdk_str(self,event_id, event_data=""):
        time_int = time.time()
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_int))
        date_int = int(time_int * 1000)
        extra_id = "%s,%s,%s,%s" % (self.serial, self.did, self.app_id, self.chanel)
        return "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
            date, event_id, event_data, self.chanel, self.did, self.cid, self.pkg_name, self.uid, self.sdk_type,
            extra_id,
            date_int, self.access_key)

    def sdk_str_without_keys(self, event_id, keys, event_data=""):
        backup = {}
        for key in keys:
            if hasattr(self, key):
                backup[key] = getattr(self, key)
                setattr(self, key, "")
        output = self.sdk_str(event_id, event_data)
        for key, value in backup.items():
            setattr(self, key, value)
        return output

    def load_vedio_success(self):
        10012
        12024
        12025
        pass
    def load_vedio_fail(self):
        10012
        12024
        12026
        pass

    def play_vedio_success(self):
        12027
        12028

    def play_vedio_success(self):
        12027
        12029

    def test_speed_success(self):
        12030
        12031

    def test_speed_fail(self):
        12030
        12032

    def load_picture_success(self):
        12022

    def load_picture_fail(self):
        12023

    def load_flower_success(self):
        12020
    def load_flower_fail(self):
        12021
    def user_continue(self):
        12019

    def user_not_continue(self):


    def wifi_to_4g(self):
        12018
    def g4_to_wifi(self):
        12018

    def  utoken_fail(self):
        pass
    def get_instance(self):
        用户校验成功
        start isinstance
        device_log

    def 
    def
    def logger_
    def loger_normal(self):
        print


    def get_device_str(self):
        return self.device.get_str()




class LogScenarios():
    @staticmethod
    def log_normal(log_request):
        """
        用户正常申请释放实例, 并包括以下事件
            refresh
            change auto
        :param log_request:
        :return:
        """

        pass

    @staticmethod
    def log_overtime(log_request):
        """
        用户申请实例，并等待游戏结束，并包括以下事件
            全屏
            退出全屏
            手动change

        :param log_request:
        :return:
        """
        pass

    def log_kicked(self):
        pass

    def log_refresh_fail(self):
        pass

    def log_change_fail(self):
        pass

    def log_not_ready(self):

test = LogRequest(1)

print test.server_str_without_keys(12312, ['cid'])
print test.server_str(12312)
print test.get_device_str()