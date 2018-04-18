#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from lib.clouddb import CloudDB
from lib.cloudamqp import CloudAMQP
from behave import *
from hamcrest import *
import time


@step(u'用户创建一个 "{status}" 的状态机')
def step_impl(context, status):
    cloud_db = CloudDB()
    cid = cloud_db.init_machine(status)
    context.scenario.current_cid = cid


@step(u'用户触发"{event_name}"事件')
def step_impl(context, event_name):
    cloud_mq = CloudAMQP()
    cloud_mq.fire_event(context.scenario.current_cid, event_name)


@step(u'这个状态机的状态应该是"{status}"')
def step_impl(context, status):
    real_status = ""
    for i in range(20):
        time.sleep(2)
        cloud_db = CloudDB()
        real_status = cloud_db.get_machine_status(context.scenario.current_cid)
        if str(real_status) == status:
            break
    assert_that(status, equal_to(str(real_status)))
