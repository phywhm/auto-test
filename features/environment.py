#!/usr/bin/env python
#-*- coding: UTF-8 -*-
from lib.clouddb import CloudDB
from lib import configuration as C
from lib import common
import os
import time

def before_scenario(context, scenario):
    scenario.current_user = None
    scenario.current_instance = None
    scenario.deleted_instance = None

    scenario.users = []
    scenario.instances = []
    scenario.deleted_instances = []
    scenario.appids = []

def after_scenario(context, scenario):
    for inst in scenario.instances:
        inst.stop_instance()

    #make sure delete the all instance when the scenarios is over
    for inst in scenario.deleted_instances:
        inst.stop_instance()

    time.sleep(5)
    del scenario.users
    del scenario.instances
    del scenario.current_user
    del scenario.current_instance
    del scenario.appids
    del scenario.deleted_instance
    params = {"operation": "test.unset.params"}
    common.run_request(context.mock_server, "POST", params)



def before_all(context):
    context.mock_server = "http://%s:%s" %(C.MOCK_SERVER, C.MOCK_PORT)
    #context.games  = CloudDB().get_games()

def after_all(context):
    del context.mock_server
#    del context.games
