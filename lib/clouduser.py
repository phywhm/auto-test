#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from base.baseinfo import BaseInfo
from cloudrequest import CloudRequest
import time


class CloudUser(object):

    def __init__(self, user, utoken, access_key='9599e53c'):
        self.user_info = BaseInfo()
        self.user_info.uid = user
        self.user_info.uToken = utoken
        self.access_key = access_key
        self.instances = []

    def start_instance(self, package_name, countly=False, **kargs):
        cloud_request = CloudRequest(self, countly, **kargs)
        kargs['pkgname'] = package_name
        cloud_request.start_instance(**kargs)
        self.instances.append(cloud_request)
        return cloud_request

    def stop_instances(self):
        for instance in self.instances:
            instance.stop_instance()



if __name__ == "__main__":
    #8F3BB845AD4   9599e53c
    clouduser01 = CloudUser('cpd125212773', '029694a0fafac97c5435a1a97a909222', "9599e53c")
    clouduser01.start_instance("com.netease.stzb.haima", False, resolution=4, client_ip='192.168.2.11')
    time.sleep(30)
    clouduser01.stop_instances()