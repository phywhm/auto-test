#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from lib.clouddb import CloudDB
from behave import *
from hamcrest import *
import time
from lib import xtestlogger
import json

logger = xtestlogger.get_logger(__name__)


_MSG_TYPES = {"kicked": 2, "waiting": 1, "confirm": 6, "refreshstoken": 11, "error": 3, "timeover": 4, "resolution": 12, "apply": 9, "ready": 10, "address": 5, "changeResolution": 12}


@step(u'这个请求应该被成功释放')
# TODO: 释放实例时, 只检查了状态, 需要更加详细的校验
def step_impl(context):
    real_status = ""
    inst = context.scenario.current_instance
    for i in range(20):
        time.sleep(2)
        cloud_db = CloudDB()
        real_status = cloud_db.get_machine_status(inst.cid)
        if str(real_status) == "Finished":
            break
    assert_that(real_status, equal_to("Finished"))


use_step_matcher("re")


@step(u'(?P<index>这个|最后一个|)请求的状态应该是"(?P<status>.*)"')
def step_impl(context, index, status):
    if index == "这个":
        cid = context.scenario.current_instance.cid
    else:
        cid = context.scenario.instances[-1].cid
    real_status = ""
    for i in range(20):
        time.sleep(2)
        cloud_db = CloudDB()
        real_status = cloud_db.get_machine_status(cid)
        if str(real_status) == status:
            break
    assert_that(status, equal_to(str(real_status)))


@step(u'第"(?P<index>[0-9]+)"个请求的状态应该是"(?P<status>.*)"')
def step_impl(context, index, status):
    index = int(index)
    inst = context.scenario.instances[index]
    real_status = ""
    for i in range(20):
        time.sleep(2)
        cloud_db = CloudDB()
        real_status = cloud_db.get_machine_status(inst.cid)
        if str(real_status) == status:
            break
    assert_that(status, equal_to(str(real_status)))


@step(u'(?P<ins_index>这个|最后一个|)请求的排队位置应该是"(?P<index>[0-9]+)"')
def step_impl(context, ins_index, index):
    if index == "这个":
        messages = context.scenario.current_instance.messages
    else:
        messages = context.scenario.instances[-1].messages
    time.sleep(60)
    wait_messages = []
    for message in messages:
        if message['operation'] == 1:
            wait_messages.append(message)
    expect_index = int(index)
    if wait_messages:
        real_index = wait_messages[-1]['data']['index']
        assert_that(real_index, equal_to(expect_index))
    else:
        assert_that(-1, equal_to(expect_index))

@step(u'第"(?P<ins_index>[0-9]+)"个请求的排队位置应该是"(?P<index>[0-9]+)"')
def step_impl(context, ins_index, index):
    time.sleep(60)
    ins_index = int(ins_index)
    messages = context.scenario.instances[ins_index].messages
    wait_messages =[]
    for message in messages:
        if message['operation'] == 1:
            wait_messages.append(message)
    expect_index = int(index)
    if wait_messages:
        real_index = wait_messages[-1]['data']['index']
        assert_that(real_index, equal_to(expect_index))
    else:
        assert_that(-1, equal_to(expect_index))


@step(u'这个(?:"(?P<type>deleted|wrong)")?实例(?P<whether>不)?应该(?P<receive>收到|包含)"(?P<message_type>.*)"消息')
def step_impl(context, type, whether,receive, message_type ):
    if type is None:
        if context.scenario.current_instance not in context.scenario.instances:  #
            if context.scenario.instances:
                context.scenario.current_instance = context.scenario.instances[-1]
            else:
                context.scenario.current_instance = context.scenario.deleted_instance
        inst = context.scenario.current_instance
    else:
        inst = context.scenario.deleted_instance
    if receive == "收到":
        for i in range(60):
            time.sleep(2)
            type_num = inst.messages[-1]['operation']
            if _MSG_TYPES[message_type] == type_num:
                break
        assert_that(_MSG_TYPES[message_type], equal_to(type_num))
    elif receive == "包含":
        for msg in context.scenario.current_instance.messages:
            if _MSG_TYPES[message_type] == msg['operation']:
                if whether is None:
                    assert_that(1, equal_to(1))
                else:
                    assert_that(1, equal_to(0))
                break
        else:
            if whether is None:
                assert_that(1, equal_to(0))
            else:
                assert_that(1, equal_to(1))


@step(u'(?P<index>这个|最后一个|)请求的"(?P<message_type>.*)"消息中(?P<whether>不)?应该包含"(?P<key>.*)"字段')
def step_impl(context, index, message_type, whether, key):
    if index == "这个":
        messages = context.scenario.current_instance.messages
    else:
        messages = context.scenario.instances[-1].messages
    tmp_msg = None
    for message in messages:
        if message['operation'] == _MSG_TYPES[message_type]:
            tmp_msg = message
            break

    tmp_msg = tmp_msg['data']
    if whether is None:
        assert_that(tmp_msg, has_key(key))
    else:
        assert_that(tmp_msg, is_not(has_key(key)))

@step(u'(?P<index>这个|最后一个|)请求的"(?P<message_type>.*)"消息中"(?P<key>.*)"字段值应该是"(?P<value>.*)"')
def step_impl(context, index, message_type,key, value):
    if index == "这个":
        messages = context.scenario.current_instance.messages
    else:
        messages = context.scenario.instances[-1].messages
    tmp_msg = None
    for message in messages:
        if message['operation'] == _MSG_TYPES[message_type]:
            tmp_msg = message
            break

    tmp_msg = tmp_msg['data']
    if key in tmp_msg:
        assert_that(tmp_msg[key], equal_to(int(value)))
    else:
        assert_that(False, equal_to(True))