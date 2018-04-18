#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from base.baseinfo import BaseInfo
from cloudrequest import CloudRequest
import time
import xtestlogger

logger = xtestlogger.get_logger(__name__)
class CloudUser(object):

    def __init__(self, user, utoken, access_key='9599e53c'):
        self.user_info = BaseInfo()
        self.user_info.uid = user
        self.user_info.uToken = utoken
        self.access_key = access_key
        self.instances = []

    def state_machine_init(self, package_name, countly=False, **kargs):
        cloud_request = CloudRequest(self, countly, **kargs)
        cloud_request.get_cid(package_name)

    def start_instance(self, package_name, countly=False, status=None ,kargs=None):
        if kargs is None:
            kargs = {}
        cloud_request = CloudRequest(self, countly, kargs)
        kargs['pkgname'] = package_name
        if status is None:
            cloud_request.start_instance(kargs)
        elif status == "Created":
            cloud_request.get_cid(kargs['pkgname'])
        elif status == "Linked":
            cloud_request.get_cid(kargs['pkgname'])
            cloud_request.websocket_connect()
        else:
            pass
        self.instances.append(cloud_request)
        return cloud_request

    def stop_instances(self):
        for instance in self.instances:
            instance.stop_instance()





if __name__ == "__main__":
    #8F3BB845AD4   9599e53c
    clouduser01 = CloudUser('cpd125212773', '029694a0fafac97c5435a1a97a909222', "xiamatest")
    clouduser01.start_instance("test.test.test")
    #clouduser01.state_machine_init("12122.121.12")
    time.sleep(20)
    clouduser01.stop_instances()