#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from lib import configuration as C
from lib import common
import time
from lib.cloudredis import CloudRedis
from lib.cloudmongo import CloudMongo
from lib.clouddb import CloudDB

def before_scenario(context, scenario):
    scenario.current_user = None
    scenario.current_instance = None
    scenario.deleted_instance = None

    scenario.users = []
    scenario.instances = []
    scenario.deleted_instances = []
    scenario.bids = []
    scenario.recv = {}
    scenario.link = {}

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
    cloud_db = CloudDB()
    cloud_mongo = CloudMongo()
    for bid in scenario.bids:
        tenant_id = cloud_db.get_tenant_id_by_bid(bid)
        cloud_mongo.remove_config_by_tenant_id(tenant_id)

    del scenario.bids
    del scenario.deleted_instance
    params = {"operation": "test.unset.params", "param": "all"}
    common.run_request(context.mock_server, "POST", params)

    #cloud_redis = CloudRedis()
    #cloud_redis.delete_keys("*")


def before_all(context):
    context.mock_server = "http://%s:%s" %(C.MOCK_SERVER, C.MOCK_PORT)
    #context.games  = CloudDB().get_games()

def after_all(context):
    del context.mock_server
#    del context.games
