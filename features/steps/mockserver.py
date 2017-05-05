#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from lib import common
from behave import *
from hamcrest import *
from lib.cloudredis import CloudRedis
from lib import xtestlogger
import json

logger = xtestlogger.get_logger(__name__)

use_step_matcher("parse")


@step(u'设置paas的最大实例数为"{num}"')
def step_impl(context, num):
    params = {"operation": "test.change.params", "max_num": num}
    common.run_request(context.mock_server, "POST", params)

@step(u'设置paas中"{router_id}"路由的实例个数为"{num}"')
def step_impl(context, router_id, num):
    num = int(num)
    params = {"operation": "test.change.params", "router_max_num": {router_id: num }}
    context.scenario.paas_request = common.run_request(context.mock_server, "POST", params)


@step(u'设置paas的回调时间为"{num}"')
def step_impl(context, num):
    params = {"operation": "test.change.params", "callback_interval": num}
    common.run_request(context.mock_server, "POST", params)


@step(u'设置paas"{action}"操作的错误响应次数为"{num}"')
def step_impl(context, action, num):
    """
    :param context:
    :param action: 设置需要控制的操作类型： ["refreshSToken", "getInterface", "release", "updateResolution":,"apply"]
    :param num: 设置失败次数
    :return:
    """
    if action == "apply":
        params = {"operation": "test.change.params", "error_operations": {'apply': int(num)}}
    elif action == "refreshSToken":
        params = {"operation": "test.change.params", "error_operations": {'refreshSToken': int(num)}}
    elif action == "getInterface":
        params = {"operation": "test.change.params", "error_operations": {'getInterface': int(num)}}
    elif action == "updateResolution":
        params = {"operation": "test.change.params", "error_operations": {'updateResolution': int(num)}}
    elif action == "release":
        params = {"operation": "test.change.params", "error_operations": {'release': int(num)}}
    else:
        pass
    common.run_request(context.mock_server, "POST", params)


@step(u'设置paas不返回回调地址')
def step_impl(context):
    params = {"operation": "test.change.params", "callback_interval": "0"}
    common.run_request(context.mock_server, "POST", params)


# TODO: mockPaas脚本还没有实现这部分
@step(u'开始记录paas收到的请求')
def step_impl(context):
    params = {"operation": "test.record.operation"}
    common.run_request(context.mock_server, "POST", params)


# TODO: mockPaas脚本还没有实现这部分, mockpaas返回operations记录并开始不记录
@step(u'获取paas收到的请求')
def step_impl(context):
    params = {"operation": "test.get.operation"}
    _, response = common.run_request(context.mock_server, "POST", params)
    context.scenario.paas_request = json.loads(response)['response']
    logger.info(context.scenario.paas_request)


@step(u'更新路由"{router}"归还实例个数为"{num}"')
def step_impl(context, router, num):
    cloud_redis = CloudRedis()
    cloud_redis.set_value('cloudservice-return-count-{router}'.format(router=router), num)



use_step_matcher("re")


@step(u'paas收到的请求中应该(?P<whether>不)?包含"(?P<operation>.*)"的请求(?:"(?P<num>[0-9]+)"次)?')
def step_impl(context,whether, operation, num):
    contain = False
    for request in context.scenario.paas_request:
        if operation in request['operation']:
            contain = True
            break
    if whether is None:
        assert_that(contain, equal_to(True))
    else:
        assert_that(contain, equal_to(False))

@step(u'paas收到的"(?P<message_type>.*)"请求中"(?P<keys>.*)"字段值应该是"(?P<value>.*)"')
def step_impl(context,message_type, keys, value):
    params = {}
    for request in context.scenario.paas_request:
        if message_type in request['operation']:
            params = request['param']

    for key in keys.split("/"):
        assert_that(params, has_key(key))
        params = params[key]

    assert_that(str(params), equal_to(value))
