#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from lib.untils import formatdata
from behave import *
import random
from lib import common
import time

@step(u'用户重复申请该实例')
def step_impl(context):
    if context.scenario.current_instance not in context.scenario.instances:
        context.scenario.current_instance = context.scenario.instances[-1]
    context.scenario.current_instance.get_instance({'confirm': 1})


use_step_matcher("re")


@step(u'用户申请一个(?:"(?P<pkg_name>random|wrong|.*)")?实例')
def step_impl(context, pkg_name=None):
    if pkg_name is None:
        pkg_name = "tests.testset." + formatdata.random_str(5)
    elif pkg_name == "random":
        pkg_name = "tests.testset." + formatdata.random_str(5)
    elif pkg_name == "wrong":
        pkg_name = "noapp.package.name"
    else:
        pass
    context.scenario.current_instance = context.scenario.current_user.start_instance(pkg_name)
    context.scenario.instances.append(context.scenario.current_instance)
    if pkg_name.lower().startswith("noapp"):
        context.scenario.deleted_instance = context.scenario.current_instance
        context.scenario.deleted_instances.append(context.scenario.current_instance)
        context.scenario.instances.remove(context.scenario.current_instance)


@step(u'用户申请一个(?:"(?P<pkg_name>random|wrong|.*)")?实例根据以下参数')
def step_impl(context, pkg_name=None):
    if pkg_name is None:
        #pkg_name = random.choice(context.games)
        pkg_name = "tests.testset." + formatdata.random_str(5)
    elif pkg_name == "random":
        pkg_name = "tests.testset." + formatdata.random_str(5)
    elif pkg_name == "wrong":
        pkg_name = "noapp.package.name"
    else:
        pass

    params = {}
    for row in context.table:
        params[row['key']] = row['value']

    context.scenario.current_instance = context.scenario.current_user.start_instance(pkg_name, kargs=params)
    context.scenario.instances.append(context.scenario.current_instance)

    if pkg_name.lower().startswith("noapp"):
        context.scenario.deleted_instance = context.scenario.current_instance
        context.scenario.deleted_instances.append(context.scenario.current_instance)
        context.scenario.instances.remove(context.scenario.current_instance)


@step(u'用户申请一个路由为"(?P<router>.*)"(?:名字为"(?P<pkg_name>random|wrong|.*)")?的实例')
def step_impl(context, router, pkg_name):
    if pkg_name is None:
        pkg_name = "tests.testset.asdf"
    elif pkg_name == "random":
        pkg_name = "tests.testset." + formatdata.random_str(5)
    elif pkg_name == "wrong":
        pkg_name = "noapp.package.name"
    else:
        pass

    params = {"operation": "test.change.params", "custom_router": router}
    common.run_request(context.mock_server, "POST", params)

    context.scenario.current_instance = context.scenario.current_user.start_instance(pkg_name)

    context.scenario.instances.append(context.scenario.current_instance)

    if pkg_name.lower().startswith("noapp"):
        context.scenario.deleted_instance = context.scenario.current_instance
        context.scenario.deleted_instances.append(context.scenario.current_instance)
        context.scenario.instances.remove(context.scenario.current_instance)

    time.sleep(10)
    params = {"operation": "test.unset.params", "param": 'custom_router'}
    common.run_request(context.mock_server, "POST", params)




@step(u'用户申请一个状态为"(?P<status>.*)"的实例')
def step_impl(context,  status):
    if context.games is None:
        pkg_name = "saas.test." + formatdata.random_str(5)
    else:
        pkg_name = random.choice(context.games)

    context.scenario.current_instance = context.scenario.current_user.start_instance(pkg_name, status=status)
    context.scenario.instances.append(context.scenario.current_instance)


@step(u'用户确认(?:第"(?P<index>[0-9]+)"个)?请求入队')
def step_impl(context, index=None):
    if index is None:
        if context.scenario.current_instance not in context.scenario.instances:
            context.scenario.current_instance = context.scenario.instances[-1]

    else:
        index = int(index)
        context.scenario.current_instance = context.scenario.instances[index]
    context.scenario.current_instance.get_instance({'confirm': 1})


@step(u'用户释放(?:第"(?P<index>[0-9]+)"个)?实例')
def step_impl(context, index=None):
    if index is None:
        if context.scenario.current_instance not in context.scenario.instances:
            context.scenario.current_instance = context.scenario.instances[-1]
        context.scenario.current_instance.stop_instance()
        context.scenario.instances.remove(context.scenario.current_instance)
        context.scenario.deleted_instance = context.scenario.current_instance
        context.scenario.deleted_instances.append(context.scenario.current_instance)
    else:
        index = int(index)
        inst = context.scenario.instances[index]
        inst.stop_instance()
        context.scenario.instances.remove(inst)
        context.scenario.deleted_instance = inst
        context.scenario.deleted_instances.append(inst)


@step(u'用户刷新(?:第"(?P<index>[0-9]+)"个)?实例的stoken')
def step_impl(context, index=None):
    if index is None:
        #   if not context.scenario.current_instance in context.scenario.instances:
        #   context.scenario.current_instance = context.scenario.instances[-1]
        context.scenario.current_instance.refresh_stoken()
    else:
        index = int(index)
        inst = context.scenario.instances[index]
        inst.refresh_stoken()
        context.scenario.current_instance = inst


@step(u'用户用"(?P<resolution>.*)"切换(?:第"(?P<index>[0-9]+)"个)?实例的码率')
def step_impl(context, resolution, index=None):
    if index is None:
        if context.scenario.current_instance not in context.scenario.instances:
            context.scenario.current_instance = context.scenario.instances[-1]
        context.scenario.current_instance.change_resolution(int(resolution))
    else:
        index = int(index)
        inst = context.scenario.instances[index]
        inst.change_resolution(int(resolution))
        context.scenario.current_instance = inst


@step(u'用户断开(?:第"(?P<index>[0-9]+)"个)?实例的长链接持续"(?P<interval>[0-9]+)"秒')
def step_impl(context, index, interval):
    interval = int(interval)
    if index is None:
        if not context.scenario.current_instance in context.scenario.instances:
            context.scenario.current_instance = context.scenario.instances[-1]
        context.scenario.current_instance.disconnected()
        time.sleep(interval)
        if interval >= 55:
            context.scenario.instances.remove(context.scenario.current_instance)
            context.scenario.deleted_instance = context.scenario.current_instance
            context.scenario.deleted_instances.append(context.scenario.current_instance)
    else:
        index = int(index)
        inst = context.scenario.instances[index]
        inst.disconnected()
        time.sleep(interval)
        if interval >= 55:
            context.scenario.instances.remove(inst)
            context.scenario.deleted_instance = inst
            context.scenario.deleted_instances.append(inst)


@step(u'用户重连(?:第"(?P<index>[0-9]+)"个)?实例的长链接')
def step_impl(context, index):
    if index is None:
        if not context.scenario.current_instance in context.scenario.instances:
            context.scenario.current_instance = context.scenario.instances[-1]
    else:
        index = int(index)
        context.scenario.current_instance = context.scenario.instances[index]
    context.scenario.current_instance.websocket_connect()


@step(u'模拟paas回调(?:第"(?P<index>[0-9]+)"个)?实例的状态为"(?P<status>.*)"')
def step_impl(context, index, status):
    if index is None:
        if not context.scenario.current_instance in context.scenario.instances:
            context.scenario.current_instance = context.scenario.instances[-1]
        context.scenario.current_instance.notify_instance(status)
        context.scenario.instances.remove(context.scenario.current_instance)
        context.scenario.deleted_instance = context.scenario.current_instance
        context.scenario.deleted_instances.append(context.scenario.current_instance)
    else:
        index = int(index)
        inst = context.scenario.instances[index]
        inst.notify_instance(status)
        context.scenario.instances.remove(inst)
        context.scenario.deleted_instance = inst
        context.scenario.deleted_instances.append(inst)