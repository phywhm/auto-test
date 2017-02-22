#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from lib.clouduser import CloudUser
from lib import common
from behave import *
from hamcrest import *
import time
import os


@step(u'I change the max instance of paas to "{num}"')
def step_impl(context, num):
    params = {"operation": "test.change.params", "max_num": num}
    common.run_request(context.mock_server, "POST", params)


@step(u'I change the callback interval of paas to "{num}"')
def step_impl(context, num):
    params = {"operation": "test.change.params", "callback_interval": num}
    common.run_request(context.mock_server, "POST", params)
