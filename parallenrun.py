#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from lib.untils import formatdata
from gevent import monkey; monkey.patch_all()
import gevent
import time
from gevent.pool import Pool
from lib.clouduser import CloudUser
import random
from gevent import getcurrent


weight = {'stop': 40, 'overtime': 40, 'crash': 10, 'noinput': 10}
interval = 180000
parallen = 200
start_time = int(time.time() * 1000)
end_time = start_time + interval
end_num = 1 + parallen
now_time = int(time.time()*1000)

def __get_do(percent):
    """
    return True or false according to the percent
    :param percent: percent is the '10' of '10%', such as: 0.1, 0.01
    :return: True or False
    """
    num = random.randint(0, 9999)
    if num in range(0, int(percent*100)):
        return True

    else:
        return False


def cloud_play(n):
    uid = "xiaom1" + formatdata.expand_int(n)
    utoken = formatdata.random_str(32)
    cloud_user = CloudUser(uid, utoken)
    playing_time = random.randint(12000, interval)
    inst = cloud_user.start_instance('test.test.te', playingTime = playing_time)
    sleep_time = random.randint(30, (end_time - now_time)/1000 + 10)

    action = 'stop'
    for key in weight.keys():
        if __get_do(weight[key]):
            action = key
            break
    #print "User: {user}; playtime: {playtime}; WaitTime: {wait}; Action:{action}".format(user=uid, playtime=playing_time,
#                                                                        wait=sleep_time, action=action)
    gevent.sleep(sleep_time)
    if action == "stop":
        inst.stop_instance()
    elif action == "noinput":
        inst.notify_instance('20')
    elif action == "crash":
        inst.notify_instance('11')
    else:
        pass
    print getcurrent()


pool = Pool(parallen)
pool.imap(cloud_play, range(1, 400))

weight['overtime'] = 0

while now_time < end_time - 30000:
    time.sleep(2)

    free_num = pool.free_count()
    print "==========", free_num
    if free_num > 0:
        pool.imap(cloud_play, range(end_num, end_num+free_num))
        end_num += free_num
    now_time = int(time.time()*1000)


