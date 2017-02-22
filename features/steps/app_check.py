#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from lib.clouddb import CloudDB
from lib.clouduser import CloudUser
from lib import common
from behave import *
from hamcrest import *
import time
import os
import json

all_types = {"kicked": 2, "waiting": 1, "confirm": 6, "refreshstoken": 11, "error": 3, "overtime": 4, "resolution": 12,
             "apply": 9, "ready": 10, "address": 5, "changeResolution": 12}

@step(u'the instance should be deleted successfully')
def step_impl(context):
    time.sleep(5)
    cloud_db = CloudDB()
    cid = context.scenario.deleted_instance.cid
    real_status = cloud_db.get_instance_status_by_cid(cid)
    assert_that(real_status, equal_to(None))
    real_cid = cloud_db.check_cid_existed(cid)
    assert_that(real_cid, equal_to(False))

@step(u'the instance is kicked from queue')
def step_impl(context):
    time.sleep(5)
    cloud_db = CloudDB()
    if context.scenario.current_instance not in context.scenario.instances:#
        context.scenario.current_instance = context.scenario.instances[-1]
    cid = context.scenario.current_instance.cid
    real_status = cloud_db.get_instance_status_by_cid(cid)
    assert_that(real_status, equal_to(None))




@step(u'the index of instance should be "{index}"')
def step_impl(context, index):
    time.sleep(60)
    messages = context.scenario.current_instance.messages
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


@step(u'the dpi of client display should be "{dpi}"')
def step_impl(context, dpi):
    time.sleep(5)
    if context.scenario.current_instance not in context.scenario.instances:#
        context.scenario.current_instance = context.scenario.instances[-1]
    cloud_db = CloudDB()
    cid = context.scenario.current_instance.cid
    display_info = cloud_db.get_display_info(cid)
    display_info = json.loads(display_info)
    if 'dpi' not in display_info['clientDisplayInfo']:
        display_info['clientDisplayInfo']['dpi'] = "null"
    expect_dpi = display_info['clientDisplayInfo']['dpi']
    assert_that(expect_dpi, equal_to(dpi))


@step(u'the resolution of client display should be "{resolution}"')
def step_impl(context, resolution):
    time.sleep(5)
    if context.scenario.current_instance not in context.scenario.instances:#
        context.scenario.current_instance = context.scenario.instances[-1]
    cloud_db = CloudDB()
    cid = context.scenario.current_instance.cid
    display_info = cloud_db.get_display_info(cid)
    display_info = json.loads(display_info)
    if 'resolution' not in display_info['clientDisplayInfo']:
        display_info['clientDisplayInfo']['resolution'] = "null"
    expect_resolution = display_info['clientDisplayInfo']['resolution']
    assert_that(expect_resolution, equal_to(resolution))

@step(u'the ID of resolution info should be "{resolution_id}"')
def step_impl(context, resolution_id):
    time.sleep(5)
    if context.scenario.current_instance not in context.scenario.instances:  #
        context.scenario.current_instance = context.scenario.instances[-1]
    cloud_db = CloudDB()
    cid = context.scenario.current_instance.cid
    params_info = cloud_db.get_display_info(cid)
    params_info = json.loads(params_info)
    expect_id = int(params_info['resolutionInfo']['id'])
    assert_that(expect_id, equal_to(int(resolution_id)))

@step(u'the resolution of resolution info should be "{resolution}"')
def step_impl(context, resolution):
    time.sleep(5)
    if context.scenario.current_instance not in context.scenario.instances:#
        context.scenario.current_instance = context.scenario.instances[-1]
    cloud_db = CloudDB()
    cid = context.scenario.current_instance.cid
    params_info = cloud_db.get_display_info(cid)
    params_info = json.loads(params_info)
    expect_resolution = params_info['resolutionInfo']['resolution']
    assert_that(expect_resolution, equal_to(resolution))

@step(u'the bit rate of resolution info should be "{bit_rate}"')
def step_impl(context, bit_rate):
    time.sleep(5)
    if context.scenario.current_instance not in context.scenario.instances:#
        context.scenario.current_instance = context.scenario.instances[-1]
    cloud_db = CloudDB()
    cid = context.scenario.current_instance.cid
    params_info = cloud_db.get_display_info(cid)
    params_info = json.loads(params_info)
    expect_resolution = int(params_info['resolutionInfo']['bitRate'])
    assert_that(expect_resolution, equal_to(int(bit_rate)))

use_step_matcher("re")
@step(u'the (?:(?P<type>deleted|wrong|) )?instance should receive "(?P<message_type>.*)" message')
def step_impl(context, message_type, type=None):
    if type is None:
        if context.scenario.current_instance not in context.scenario.instances:  #
            if context.scenario.instances:
                context.scenario.current_instance = context.scenario.instances[-1]
            else:
                context.scenario.current_instance = context.scenario.deleted_instance
        inst = context.scenario.current_instance
    else:
        inst = context.scenario.deleted_instance
    for i in range(60):
        time.sleep(2)
        type_num = inst.messages[-1]['operation']
        if all_types[message_type] == type_num:
            break

    assert_that(all_types[message_type], equal_to(type_num))

use_step_matcher("re")
@step(u'the status of(?: (?P<type>deleted|wrong))? instance should be "(?P<status>[0-9]+)"')
def step_impl(context, status, type=None):
    if type is None:
        if context.scenario.current_instance not in context.scenario.instances:  #
            if context.scenario.instances:
                context.scenario.current_instance = context.scenario.instances[-1]
            else:
                context.scenario.current_instance = context.scenario.deleted_instance
        inst = context.scenario.current_instance
    else:
        inst = context.scenario.deleted_instance
    for i in range(20):
        time.sleep(2)
        cloud_db = CloudDB()
        cid = inst.cid
        real_status = cloud_db.get_instance_status_by_cid(cid)
        if str(real_status) == status:
            break
    assert_that(status, equal_to(str(real_status)))



@step(u'the wait message should(?: (?P<flag>not))? contain "(?P<key>.*)"')
def step_impl(context, key, flag=None):
    time.sleep(60)
    messages = context.scenario.current_instance.messages
    wait_messages =[]
    for message in messages:
        if message['operation'] == 1:
            wait_messages.append(message)
    if wait_messages:
        data = wait_messages[-1]['data']
        if flag  is None:
            assert_that(data, has_key(key))
        else:
            if data.has_key("key"):
                assert_that("not timeStr key", equal_to("timeStr key"))
    else:
        assert_that("receive wait message", equal_to("None wait message"))


@step(u'the instance should(?: (?P<flag>not))? contain "(?P<message_type>.*)" message(?: "(?P<count>[0-9]+)" times)?')
def step_impl(context, message_type):
    time.sleep(10)
    if context.scenario.current_instance not in context.scenario.instances:
        context.scenario.current_instance = context.scenario.instances[-1]

    for msg in context.scenario.current_instance.messages:
        if all_types[message_type] == msg['operation']:
            assert_that(1, equal_to(1))
            return
    assert_that(1, equal_to(0))