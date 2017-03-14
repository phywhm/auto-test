#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from datetime import *
from lib.cloudtools import stop_service
from lib.cloudtools import recover_server


@step(u'I send maintenance message for "{interval}" minutes in "{future}" minutes')
def step_impl(interval, future):
    begin_time = datetime.now() + timedelta(minutes=int(future)).isoformat(" ")
    end_time = begin_time + timedelta(minutes=int(interval)).isoformat(" ")
    stop_service(begin_time, end_time)

@step(u'I recover the service right now')
def step_impl():
    recover_server()