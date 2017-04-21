#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from lib.clouduser import CloudUser
from lib.clouddb import CloudDB
from lib.cloudredis import CloudRedis
from lib.untils import formatdata
from behave import *
from hamcrest import *
import time

use_step_matcher("parse")
@step(u'玩家通过租户"{access_key}"注册一个用户')
def step_impl(context, access_key):
    cloud_db = CloudDB()
    cloud_redis = CloudRedis()
    user = "xTest" + formatdata.random_str(4)
    context.scenario.current_user = CloudUser(user, "password", access_key)
    context.scenario.users.append(context.scenario.current_user)
    context.scenario.order_id = cloud_db.get_order_by_accesskey(access_key)

    if access_key not in context.scenario.appids:
        cloud_db.set_concurrency_by_accesskey(access_key, 1000)
        cloud_redis.set_value("cloudservice-count-" + context.scenario.order_id, "500")
        context.scenario.appids.append(access_key)
        time.sleep(2)


use_step_matcher("re")
@step(u'I switch to the "(?P<index>[0-9]+)th" user')
def step_impl(context, index):
    context.scenario.current_user  =  context.scenario.users[int(index)]
    context.scenario.current_instance  =  context.scenario.current_user.instances[-1]
