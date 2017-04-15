#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from lib import common
from behave import *
from hamcrest import *


use_step_matcher("parse")


@step(u'设置paas的最大实例数为"{num}"')
def step_impl(context, num):
    params = {"operation": "test.change.params", "max_num": num}
    common.run_request(context.mock_server, "POST", params)


@step(u'设置paas的回调时间为"{num}"')
def step_impl(context, num):
    params = {"operation": "test.change.params", "callback_interval": num}
    common.run_request(context.mock_server, "POST", params)


@step(u'设置paas的错误响应次数为"{num}"')
def step_impl(context, num):
    params = {"operation": "test.change.params", "max_error_times": num}
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
    params = {"operation": "test.record.operation"}
    common.run_request(context.mock_server, "POST", params)


use_step_matcher("re")


@step(u'paas的请求中(?P<key>不)?包含"(?P<operation>.*)"的请求')
def step_impl(context, key, operation):
    contain = False
    for request in context.scenario.paas_request:
        if request['operation'] == operation:
            contain = True
            break
    if key is None:
        assert_that(contain, equal_to(True))
    else:
        assert_that(contain, equal_to(False))

