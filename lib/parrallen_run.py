#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from threading import Thread
from untils import formatdata

class MutiUser(Thread):
    PLAY_TIME = 300000
    def __init__(self, parallel_num, access_key='xiamatest', min_playtime=300000,max_playtime=360000):
        self.users = []
        for i in range(parallel_num):
            userrequest = {}
            uid = access_key + formatdata.expand_int(i)
            utoken = formatdata.random_str(32)
            clouduser = CloudUser(uid, utoken, access_key)
            userrequest['user'] = clouduser

            # userrequest['package'] = common.random_str(40)
            userrequest['package'] = "com.jimei.xsanguo.haima"
            userrequest['priority'] = common.random_int(100, 10000)
            userrequest['playtime'] = common.random_int(min_playtime, max_playtime)
            userrequest['waiting'] = True
            #游戏overtime后,使用调用stop
            userrequest['intervel'] = max_playtime + 60000

            self.user.append(userrequest)

    def run(self):
