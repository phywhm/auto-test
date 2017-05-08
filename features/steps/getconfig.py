#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from lib.clouddb import CloudDB
from lib.cloudmongo import CloudMongo
from lib import common
from behave import *
from hamcrest import *
import time
import json

@step(u'I get the configuration')
def step_impl(context):
    context.output = context.scenario.current_user.get_config()


@step(u'the vaule of "{key}" should be "{content}" in tips')
def step_impl(context, key, content):
    tips_out = dict([(x['k'], x['v']) for x in context.output['interactiveTalkInfo']])
    assert_that(tips_out, instance_of(dict))
    assert_that(tips_out, has_entry(key, content))


@step(u'the talkinfo of configuration should contain')
def step_impl(context):
    talk_info = dict([(x['k'], x['v']) for x in context.output['interactiveTalkInfo']])
    for row in context.table:
        assert_that(talk_info, has_entry(row['key'],row['value']))

@step(u'设置接入商"{bid}"的"{key}"配置值为"{value}"')
def step_impl(context, bid, key, value):
    cloud_db = CloudDB()
    tenant_id = cloud_db.get_tenant_id_by_bid(bid)
    cloud_mongo = CloudMongo()
    if key in ['showEstimateTime', 'appCallback']:
        if value in ["False",  "false"]:
            value = False
        elif value in ['True', 'true']:
            value = True
        params = {key: bool(value)}
    else:
        params = {'sdkConfig': {key: value} }
    cloud_mongo.create_config_by_tenant_id(tenant_id, params)
