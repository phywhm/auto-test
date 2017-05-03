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

    def get_value(self, key):
        if self.redis_conn.type(key) == "zset":
            return self.redis_conn.zrange(key,0, -1)
        elif self.redis_conn.type(key) == "string":
            return self.redis_conn.get(key)
        elif self.redis_conn.type(key) == "list":
            return self.redis_conn.lrange(key,0,-1)
        elif self.redis_conn.type(key) == "list":
            return self.redis_conn.hgetall(key)

    def get_type(self,key):
        return self.redis_conn.type(key)

    def set_value(self, key, value):
        self.redis_conn.set(key, value)
        self.redis_conn.save()


    def get_sort_queue(self, key):
        return self.redis_conn.zrange(key, 0, -1)




if __name__ == "__main__":
    os.environ["REDIS_HOST"] = "172.16.2.16"
    cloud_redis = CloudRedis()
    #cloud_redis.set_wait_time()
    #cloud_redis.delete_keys("APP_GLOBAL_CONFIG*")
    #for key in cloud_redis.get_keys("countly_wait_start_time_*"):
    #    print key, cloud_redis.get_ttl(key)
    #    if cloud_redis.get_ttl(key) is not None:
    #        print key, cloud_redis.get_ttl(key)
    #cloud_redis.delete_keys("saas_access_fail_message_to_*")+
    for key in cloud_redis.get_keys("cloudservice-queue-*"):
        print key,cloud_redis.get_value(key)
    for key in cloud_redis.get_keys("channel-context*"):
        print key, cloud_redis.get_value(key)

    for key in cloud_redis.get_keys("cloudservice-return-count-*"):
        print key, cloud_redis.get_value(key)

        #cloud_redis.set_value("cloudservice-count-12", "244")
        #cloud_redis.delete_keys("channel-context*")
    #cloud_redis.delete_keys("cloudservice-queue-*")
    #print cloud_redis.get_vaule("APP_GLOBAL_CONFIG_xiamatest")
    #print cloud_redis.get_avgwait_time()
    #print cloud_redis.get_totalwait_user()
