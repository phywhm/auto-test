#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
from constants import *
import redis
import configuration as CONFIG


class CloudRedis(object):
    def __init__(self, host=None, port=6379, db=0, password=None):
        reload(CONFIG)
        if host:
            self.redis_conn = redis.Redis(host=host, port=port, db=db, password=password)
        else:
            self.redis_conn = redis.Redis(host=CONFIG.REDIS_HOST, port=CONFIG.REDIS_PORT, db=CONFIG.REDIS_DB,
                                          password=CONFIG.REDIS_PASSWD)

    def delete_keys(self, pattern):
        keys = self.redis_conn.keys(pattern)
        for key in keys:
            self.redis_conn.delete(key)
        self.redis_conn.save()

    def get_keys(self, pattern):
        return self.redis_conn.keys(pattern)

    def delete_wait_time_key(self):
        self.redis_conn.delete(TOTAL_WAIT_USER_DATA_KEY)
        self.save()

    def get_totalwait_time(self):
        return  self.redis_conn.hget(TOTAL_WAIT_USER_DATA_KEY, TOTAL_WAIT_TIME_KEY)

    def get_totalwait_user(self):
        return self.redis_conn.hget(TOTAL_WAIT_USER_DATA_KEY, TOTAL_WAIT_USERS_KEY)

    def get_avgwait_time(self):
        return self.redis_conn.hget(TOTAL_WAIT_USER_DATA_KEY, AVG_WAIT_TIME_KEY)

    def get_ttl(self, key):
        return self.redis_conn.ttl(key)

    def set_wait_time(self):
        self.redis_conn.hset(TOTAL_WAIT_USER_DATA_KEY, TOTAL_WAIT_TIME_KEY, "1212400000")
        self.redis_conn.hset(TOTAL_WAIT_USER_DATA_KEY, TOTAL_WAIT_USERS_KEY, "2")
        self.redis_conn.hset(TOTAL_WAIT_USER_DATA_KEY, AVG_WAIT_TIME_KEY, "66200000")

    def get_vaule(self,key):
        print self.redis_conn.type(key)
        return self.redis_conn.get(key)



if __name__ == "__main__":
    os.environ["REDIS_HOST"] = "172.16.2.90"
    cloud_redis = CloudRedis()
    #cloud_redis.set_wait_time()
    #cloud_redis.delete_keys("APP_GLOBAL_CONFIG*")
    #for key in cloud_redis.get_keys("countly_wait_start_time_*"):
    #    print key, cloud_redis.get_ttl(key)
    #    if cloud_redis.get_ttl(key) is not None:
    #        print key, cloud_redis.get_ttl(key)
    #cloud_redis.delete_keys("saas_access_fail_message_to_*")
    for key in cloud_redis.get_keys("APP_GLOBAL_CONFIG*"):
        print key, cloud_redis.get_ttl(key)
    #cloud_redis.delete_keys("APP_GLOBAL_CONFIG*")
    print cloud_redis.get_vaule("APP_GLOBAL_CONFIG_xiamatest")
    #print cloud_redis.get_avgwait_time()
    #print cloud_redis.get_totalwait_user()
