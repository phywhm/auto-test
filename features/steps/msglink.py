#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time

from behave import *
from hamcrest import assert_that, equal_to, greater_than_or_equal_to, less_than_or_equal_to, starts_with

from lib import xtestlogger
from lib.cloudamqp import CloudAMQP
from lib.clouddb import CloudDB
from lib.cloudredis import CloudRedis
from lib.linkrequest import LinkRequest

logger = xtestlogger.get_logger("msg_link")


@Given(u"使用CID {cid} 连接长连接服务器")
def step_impl(context, cid):
    context.recv = []
    context.link = {cid: LinkRequest(cid, context)}
    context.link[cid].websocket_connect()
    time.sleep(1)


@Then(u"检查 {cid} 路由是否在消息中心注册成功")
def step_impl(context, cid):
    redis = CloudRedis()
    link = eval(redis.get_link_by_cid(cid))
    logger.info("cid %s link route is %s" % (cid, link))
    assert link is not None
    assert_that(link, starts_with('link'), "link route is %s" % link)
    assert_that(len(link), less_than_or_equal_to(6), "link route is %s and length > 6" % link)
    assert_that(len(link), greater_than_or_equal_to(5), "link route is %s and length < 5" % link)
    time.sleep(1)


@Then(u"清除CID {cid} 的所有消息")
def step_impl(context, cid):
    db = CloudDB()
    db.clear_msg_for_cid(cid)
    time.sleep(1)


@Then(u"推送单播消息 {msg} 给 {cid} 客户端")
def step_impl(context, msg, cid):
    mq_client = CloudAMQP()
    mq_client.push_single_msg(cid, msg)
    time.sleep(1)


@When(u"当 {cid} 客户端收到消息 {msg}")
def step_impl(context, cid, msg):
    for i in range(10):
        if context.recv and len(context.recv) > 0:
            tmp = context.recv.pop()
            assert_that(tmp, msg, "context %s" % tmp)
            break
        else:
            time.sleep(0.5)
            if i == 9:
                assert_that(1, equal_to(0), "context %s" % context.recv)


@Then(u"检查数据库中 {cid} 的消息状态是否为 {sts}")
def step_impl(context, cid, sts):
    mcdb = CloudDB()
    tmp_sts = mcdb.get_last_msg_status_by_cid(cid)
    assert_that(tmp_sts, sts, "record status %s not expected %s" % (tmp_sts, sts))


@Then(u"{cid} 客户端主动断开长连接")
def step_impl(context, cid):
    context.link[cid].disconnected()
    time.sleep(2)


@Then(u"检查 {cid} 路由是否在消息中心注销成功")
def step_impl(context, cid):
    redis = CloudRedis()
    link = redis.get_link_by_cid(cid)
    logger.info("cid %s link route is %s and it should be None" % (cid, link))
    assert link is None


@Then(u"踢出CID为 {cid} 的用户")
def step_impl(context, cid):
    mq = CloudAMQP()
    mq.kick_client(cid)
    time.sleep(1)


@Then(u"将 {cid} 调整分组至 {group_list}")
def step_impl(context, cid, group_list):
    mq = CloudAMQP()
    mq.alloc_group(cid, group_list)
    time.sleep(1)


@Step(u"推送组消息 {msg} 至 {group_list}")
def step_impl(context, msg, group_list):
    mq_client = CloudAMQP()
    mq_client.push_group_msg(group_list, msg)
    time.sleep(1)
