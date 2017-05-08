#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from behave import *

from lib.cloudamqp import CloudAMQP


@Given("use cid {cid} connect link")
def step_impl(context, cid):
    pass


@Then("send msg {msg} to client with cid {cid}")
def step_impl(context, msg, cid):
    mq_client = CloudAMQP()
    mq_client.push_single_msg(cid, msg)


@When("client with cid {cid} receive msg tmsg")
def step_impl(context, cid):
    pass


@Then("client with cid {cid} disconnect")
def step_impl(context, cid):
    pass


@Then("kick off client with cid {cid}")
def step_impl(context, cid):
    pass


@Then("alloc cid {cid} group {group_list}")
def step_impl(context, cid, group_list):
    pass


@Then("push group msg {msg} to group {group_list}")
def step_impl(context, group_list, msg):
    mq_client = CloudAMQP()
    mq_client.push_group_msg(group_list, msg)