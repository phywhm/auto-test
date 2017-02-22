#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from lib.clouduser import CloudUser
from lib.clouddb import CloudDB
from lib.untils import formatdata
from behave import *
from hamcrest import *
import time
import os

@step(u'I registry an user with "{access_key}" access key')
def step_impl(context, access_key):
    cloud_db = CloudDB()
    user = "xTest" + formatdata.random_str(4)
    context.scenario.current_user = CloudUser(user, "password", access_key)
    context.scenario.users.append(context.scenario.current_user)
    if access_key not in context.scenario.appids:
        cloud_db.update_access_limit(access_key)
        context.scenario.appids.append(access_key)
        time.sleep(3)


use_step_matcher("re")
@step(u'I switch to the "(?P<index>[0-9]+)th" user')
def step_impl(context, index):
    context.scenario.current_user  =  context.scenario.users[int(index)]
    context.scenario.current_instance  =  context.scenario.current_user.instances[-1]
