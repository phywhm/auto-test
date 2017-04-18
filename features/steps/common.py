#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from lib.clouddb import CloudDB
from lib.cloudredis import CloudRedis
from lib.untils import formatdata
from behave import *
from hamcrest import *
import time


@step(u'等待"{interval}"毫秒')
def step_impl(context, interval):
    time.sleep(int(interval)/1000)


@step(u'随机等待很小一段时间')
def step_impl(context):
    interval = formatdata.random_int(100, 1500)
    time.sleep(int(interval)/1000)


@step(u'设置接入商"{access_key}"的实例上限和已用是个个数分别为"{limit}"和"{count}"')
def step_impl(context, limit, count, access_key):
    cloud_db = CloudDB()
    # limit = int(limit)
    # count = int(count)
    cloud_redis = CloudRedis()
    cloud_redis.set_value("cloudservice-count-12", count)


@step(u'接入商"{access_key}"已占用的实例个数应该为"{num}"')
def step_impl(context, access_key, num):
    time.sleep(2)
    cloud_redis = CloudRedis()
    instance_num = cloud_redis.get_value("cloudservice-count-12")
    if num == "default":
        assert_that(instance_num, equal_to('500'))
    else:
        assert_that(instance_num, equal_to(num))
