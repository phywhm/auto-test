#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from lib.clouddb import CloudDB
from lib import common
from lib.untils import formatdata
from behave import *
from hamcrest import *
import time
from lib.cloudamqp import CloudAMQP
import random


@step(u'I delete the record of instance from database')
def step_impl(context):
    if context.scenario.current_instance not in context.scenario.instances:
        context.scenario.current_instance = context.scenario.instances[-1]
    cloud_db = CloudDB()
    cid = context.scenario.current_instance.cid
    cloud_db.delete_instance_record(cid)

@step(u'I stop the instance without check')
def step_impl(context):
    if context.scenario.current_instance not in context.scenario.instances:
        context.scenario.current_instance = context.scenario.instances[-1]
    context.scenario.current_instance.stop_instance(check=False)
    context.scenario.instances.remove(context.scenario.current_instance)
    context.scenario.deleted_instance = context.scenario.current_instance


@step(u'I re-request the app again')
def step_impl(context):
    if context.scenario.current_instance not in context.scenario.instances:
        context.scenario.current_instance = context.scenario.instances[-1]
    context.scenario.current_instance.get_instance(confirm=1)


@step(u'I start and stop the instance in the short time for "{num}" times')
def step_impl(context, num):
    for x in range(1, int(num)):
        context.execute_steps(u"""
            Given I registry an user with "xiamatest" access key
            When I request a app
            And I wait a short time
            Then I stop the instance without check
            And I wait "10" ms
        """)



@step(u'I start and stop the instance normally for "{num}" times')
def step_impl(context, num):
    for x in range(1, int(num)):
        context.execute_steps(u"""
            When I request a app
            Then the status of instance should be "4"
            Then I try to stop the instance
        """)

@step(u'I disconnet the websocket of instance for "{interval}" seconds')
def step_impl(context, interval):
    interval = int(interval)
    if not context.scenario.current_instance in context.scenario.instances:
        context.scenario.current_instance = context.scenario.instances[-1]
    context.scenario.current_instance.disconneted()
    time.sleep(interval)
    if interval >= 55:
        context.scenario.instances.remove(context.scenario.current_instance)
        context.scenario.deleted_instance = context.scenario.current_instance
        context.scenario.deleted_instances.append(context.scenario.current_instance)

@step(u'I reconnect the websocket of instance')
def step_impl(context):
    if not context.scenario.current_instance in context.scenario.instances:
        context.scenario.current_instance = context.scenario.instances[-1]
    context.scenario.current_instance.websocket_connect()

@step(u'I wait "{interval}" ms for overtime')
def step_impl(context, interval):
    time.sleep(int(interval)/1000)
    context.scenario.deleted_instance = context.scenario.current_instance
    context.scenario.deleted_instances.append(context.scenario.current_instance)



use_step_matcher("re")
@step(u'I request a (?:"(?P<pkg_name>random|wrong|.*)" )?app')
def step_impl(context, pkg_name=None):
    if pkg_name is None:
        pkg_name = "tests.testset.asdf"
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

@step(u'I request an (?:"(?P<pkg_name>random|wrong|.*)" )?app with')
def step_impl(context, pkg_name=None):
    if pkg_name is None:
        pkg_name = random.choice(context.games)
    elif pkg_name == "random":
        pkg_name = "tests.testset." + formatdata.random_str(5)
    elif pkg_name == "wrong":
        pkg_name = "noapp.package.name"

    else:
        pass

    params = {}
    for row in context.table:
        params[row['key']] = row['value']

    context.scenario.current_instance = context.scenario.current_user.start_instance(pkg_name, **params)
    context.scenario.instances.append(context.scenario.current_instance)

    if pkg_name.lower().startswith("noapp"):
        context.scenario.deleted_instance = context.scenario.current_instance
        context.scenario.deleted_instances.append(context.scenario.current_instance)
        context.scenario.instances.remove(context.scenario.current_instance)


@step(u'I request a (?:"(?P<pkg_name>random|wrong|.*)" )?app without confirm')
def step_impl(context, pkg_name=None):
    if pkg_name is None:
        pkg_name = "tests.testset.asdf"
    elif pkg_name == "random":
        pkg_name = "tests.testset." + formatdata.random_str(5)
    elif pkg_name == "wrong":
        pkg_name = "noapp.package.name"
    else:
        pass

    context.scenario.current_instance = context.scenario.current_user.start_instance(pkg_name, waiting=False)
    context.scenario.instances.append(context.scenario.current_instance)
    if pkg_name.lower().startswith("noapp"):
        context.scenario.deleted_instance = context.scenario.current_instance
        context.scenario.deleted_instances.append(context.scenario.current_instance)
        context.scenario.instances.remove(context.scenario.current_instance)


@step(u'I request a (?:"(?P<pkg_name>random|wrong|.*)" )?app with "(?P<route>.*)" route')
def step_impl(context, route, pkg_name=None):
    if pkg_name is None:
        pkg_name = "tests.testset.asdf"
    elif pkg_name == "random":
        pkg_name = "tests.testset." + formatdata.random_str(5)
    elif pkg_name == "wrong":
        pkg_name = "noapp.package.name"
    else:
        pass

    params = {"operation": "test.set.route", "routes": route}
    common.run_request(context.mock_server, "POST", params)

    context.scenario.current_instance = context.scenario.current_user.start_instance(pkg_name)

    context.scenario.instances.append(context.scenario.current_instance)

    if pkg_name.lower().startswith("noapp"):
        context.scenario.deleted_instance = context.scenario.current_instance
        context.scenario.deleted_instances.append(context.scenario.current_instance)
        context.scenario.instances.remove(context.scenario.current_instance)

    time.sleep(10)
    params = {"operation": "test.unset.route", "routes": route}
    common.run_request(context.mock_server, "POST", params)


@step(u'I request a (?:"(?P<pkg_name>random|wrong|.*)" )?app with "(?P<param>[0-9]+)" (?P<key>priority|time)')
def step_impl(context, param, key, pkg_name=None):
    if pkg_name is None:
        pkg_name = "tests.testset.asdf"
    elif pkg_name == "random":
        pkg_name = "tests.testset." + formatdata.random_str(5)
    elif pkg_name == "wrong":
        pkg_name = "noapp.package.name"
    else:
        pass

    if key == "priority":
        context.scenario.current_instance = context.scenario.current_user.start_instance(pkg_name, priority=param)
    elif key == "time":
        context.scenario.current_instance = context.scenario.current_user.start_instance(pkg_name, playingTime=param)
    else:
        context.scenario.current_instance = context.scenario.current_user.start_instance(pkg_name)

    context.scenario.instances.append(context.scenario.current_instance)

    if pkg_name.lower().startswith("noapp"):
        context.scenario.deleted_instance = context.scenario.current_instance
        context.scenario.deleted_instances.append(context.scenario.current_instance)
        context.scenario.instances.remove(context.scenario.current_instance)


@step(u'I try to stop the (?:"(?P<index>[0-9]+)th" )?instance')
def step_impl(context, index=None):
    if index is None:
        if not context.scenario.current_instance in context.scenario.instances:
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




@step(u'I notify the (?:"(?P<index>[0-9]+)th" )?instance with "(?P<status>.*)" status')
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

@step(u'I notify the first real instance with "(?P<status>.*)" status')
def step_impl(context, status):
    for inst in context.scenario.instances:
        inst.notify_instance(status)
        context.scenario.instances.remove(inst)
        context.scenario.deleted_instances.append(inst)
        context.scenario.deleted_instance = inst
        break


@step(u'I disconnet websocket for the (?:"(?P<index>[0-9]+)th" )?instance')
def step_impl(context, index):
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
        inst.disconnected()
        context.scenario.instances.remove(inst)
        context.scenario.deleted_instance = inst
        context.scenario.deleted_instances.append(inst)


@step(u'I refresh the stoken of (?:"(?P<index>[0-9]+)th" )?instance')
def step_impl(context, index=None):
    if index is None:
#        if not context.scenario.current_instance in context.scenario.instances:
#            context.scenario.current_instance = context.scenario.instances[-1]
        context.scenario.current_instance.refresh_stoken()
    else:
        index = int(index)
        inst = context.scenario.instances[index]
        inst.refresh_stoken()
        context.scenario.current_instance = inst


@step(u'I change the resolution of (?:"(?P<index>[0-9]+)th" )?instance with the "(?P<resolution_id>[0-9]+)th" ID')
def step_impl(context,resolution_id, index=None):
    if index is None:
        if not context.scenario.current_instance in context.scenario.instances:
            context.scenario.current_instance = context.scenario.instances[-1]
        context.scenario.current_instance.change_resolution(int(resolution_id))
    else:
        index = int(index)
        inst = context.scenario.instances[index]
        inst.change_resolution(int(resolution_id))
        context.scenario.current_instance = inst
