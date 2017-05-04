#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pymongo
import configuration as CONFIG


class CloudMongo(object):

    def __init__(self, host=None, port=27017):
        if host:
            self.mongo_client = pymongo.MongoClient(host=host, port=port)
        else:
            self.mongo_client = pymongo.MongoClient(host=CONFIG.MONGO_HOST, port=CONFIG.MONGO_PORT)

    def __use_mongo(self, db, user, password):
        db = self.mongo_client[db]
        db.authenticate(user, password)
        return db



    def create_config_by_tenant_id(self, tenant_id, data):
        db = self.__use_mongo(CONFIG.CONFIG_DB,CONFIG.MONGO_USER, CONFIG.MONGO_PASSWORD)
        tmp_collection = db['CloudServiceProductConfig']
        tmp_collection.remove({"tenantId": int(tenant_id)})
        tmp_collection.insert(data)

    def remove(self, collection, params=None):
        if params is None:
            params = {}

        db = self.__use_mongo()
        table = db[collection]
        table.remove(params)

    def insert(self, collection, data):
        db = self.__use_mongo()
        table = db[collection]
        table.insert(data)

    def find(self, collection, params=None):
        db = self.__use_mongo('db_tenant_test', 'admin', '123qwe')
        table = db[collection]
        if params is None:
            return table.find()
        else:
            return table.find(params)

if __name__ == "__main__":
    mongo = CloudMongo()
    mongo.create_config_by_tenant_id(4,
                                     { "_class": "com.haima.cloudplayer.tenantmgt.dal.mongo.model.CloudServiceProductConfigDo",
                                      "tenantId": 4,
                                      "envId": 0,
                                      "clientType": 0,
                                      "cloudServiceProductId": 0,
                                      "config":
                                          {"flagStartSpeedTest": True}
                                      })