#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from lib.clouddb import CloudDB
from lib.untils import formatdata
from behave import *
from hamcrest import *
import time


@step('等待"{interval}"毫秒')
def step_impl(context, interval):
    time.sleep(int(interval)/1000)


@step(u'I wait a short time')
def step_impl(context):
    interval = formatdata.random_int(100, 1500)
    time.sleep(int(interval)/1000)


@step(u'I update the instance limit to {limit} and count to {count} on "{access_key}" access key')
def step_impl(context, limit, count, access_key):
    cloud_db = CloudDB()
    # limit = int(limit)
    # count = int(count)
    cloud_db.update_access_limit(access_key, limit, count)
    time.sleep(3)


@step(u'接入商"{access_key}"的实例个数应该为"{num}"')
def step_impl(context, access_key, num):
    time.sleep(5)
    cloud_db = CloudDB()
    instance_num = cloud_db.get_access_limit(access_key)
    if num == "default":
        assert_that(instance_num, equal_to(500))
    else:
        assert_that(instance_num, equal_to(int(num)))
