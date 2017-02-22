#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import configuration as CONFIG
import requests
from untils import formatdata
import json
import threading
import time
import inspect
from constants import *
from websocket import create_connection
import encryption
import common
from clouddb import CloudDB
from countly import CloudCountly
from countly import pre_events
from countly import process_event
import xtestlogger
from cloud_config import get_ctoken_backdoor


logger = xtestlogger.get_logger(__name__)

class CloudRequestException(Exception):
    def __init__(self, msg):
        self.message = msg


class RequestParamException(Exception):
    def __init__(self, msg):
        self.message = msg


class WebSocketException(Exception):
    def __init__(self, msg):
        self.message = msg


class CloudRequest(object):
    def __init__(self, cloud_user, countly=False, **kargs):
        reload(CONFIG)
        self.cloud_user = cloud_user
        self.sdk_type = None
        self.did = None
        self.cid = None
        self.sign = None
        self.socket_url = None
        self.secret_key = None
        self.device = None
        self.client = requests.generate_client_info()
        self.data = None
        self.socket = None
        self.countly = countly
        self.cloud_countly = None
        self.extra_id = None
        self.ctoken_backdoor = 'abcd'

        self.user_info = cloud_user.user_info
        self.access_key = cloud_user.access_key
        self.priority = 0
        self.playing_time = 3000000
        self.protocol = CONFIG.PROTOCOL_VERSION
        self.messages = []
        self.timer = None
        self.device_id = formatdata.random_str(32)

        self.url = "http://" + CONFIG.SAAS_HOST + ":" + CONFIG.SAAS_PORT + '/s/rest/api'
        self.status = INSTANCE_NOT_REQUEST
        if self.access_key is not None:
            self.client.accessKeyID = self.access_key


        self.registry_sdk(**kargs)

    def __clould_request(self, params):
        try:
            params = encryption.encrypt_cloud_request(params, self.secret_key)
            return common.run_request(self.url, method="POST", commparams=params)
        except Exception as e:
            raise CloudRequestException("Fail Action: %s; Reason: %s" % (inspect.stack()[1][3], e.message))

    def __cloud_json_check(self, res):
        if res['code'] != 0:
            if inspect.stack()[1][3] in ['registry_sdk', 'get_cid']:
                msg = "Fail Action: %s; Reason: %s" % (inspect.stack()[1][3], res['msg'])
            else:
                msg = "cid-%s Fail Action: %s; Reason: %s" % (self.cid, inspect.stack()[1][3], res['msg'])
            raise RequestParamException(msg)
        else:
            res = requests.convert_dict(res)
            res = encryption.decrypt_cloud_response(res, self.secret_key)
            return res

    def registry_sdk(self, **kargs):
        if 'os_type' in kargs:
            self.sdk_type = int(kargs['os_type'])
        else:
            self.sdk_type = formatdata.random_int(1, 5)

        # generate the  request body
        params = requests.generate_comm_request(ACTION_DID_REGISTER, self.sdk_type, self.protocol)
        self.device = requests.generate_device_info(self.sdk_type)
        params.device = self.device
        params.client = self.client
        params.data.type = self.sdk_type

        if 'client_resolution' in kargs:
            params.device.screenInfo.resolution = kargs['client_resolution']
        if 'dpi' in kargs:
            params.device.screenInfo.dpi = kargs['dpi']

        if 'model' in kargs:
            params.device.model = kargs['model']

        status, respone = self.__clould_request(params)
        res = json.loads(respone)
        res = self.__cloud_json_check(res)
        self.did = res['data']['did']

    def get_config(self):
        params = requests.generate_comm_request(ACTION_GET_CONFIGURE, self.sdk_type, self.protocol, self.did)
        params.data.accessKeyID = self.access_key

        status, respone = self.__clould_request(params)
        res = json.loads(respone)
        res = self.__cloud_json_check(res)
        if self.countly:
            self.extra_id = "{serial},{device},{game},{channel}".format(serial=formatdata.random_str(32),
                                                                        device=self.device_id,
                                                                        game=formatdata.random_str(6, '12345567890'),
                                                                        channel=self.client.channel)
            self.cloud_countly = CloudCountly("http://172.16.2.77", "8f1680f2ab51d0a0db291277080c9c46ab6ab638",
                                              self.device_id, self.sdk_type)
        #print res['data']['setDataInfo']
        #self.ctoken_backdoor = res['data']['setDataInfo']['ctoken_status_flag']
        return res['data']

    def get_cid(self, package_name):
        params = requests.generate_comm_request(ACTION_CID, self.sdk_type, self.protocol, self.did)
        params.client = self.client
        params.data.userInfo = self.user_info
        params.data.pkgName = package_name
        if CONFIG.USE_CTOKEN_BACKDOOR:
            params.data.CToken = self.ctoken_backdoor
        else:
            params.data.CToken = encryption.generate_ctoken(params)
        params.data.configInfo = formatdata.random_str(200)

        status, respone = self.__clould_request(params)
        res = json.loads(respone)
        res = self.__cloud_json_check(res)
        self.cid = res['data']['cidId']
        self.sign = res['data']['sign']
        self.socket_url = res['data']['msgServInfo']['socketUrl']
        if 'secretKey' in res['data']:
            self.secret_key = res['data']['secretKey']

    def get_instance(self, **kargs):
        logger.warning(kargs)
        params = requests.generate_comm_request(ACTION_GET_CLOUD_SERVICE, self.sdk_type, self.protocol, self.did)
        if 'playingTime' not in kargs:
            kargs['playingTime'] = self.playing_time
        else:
            self.playing_time = kargs['playingTime']
        if 'priority' not in kargs:
            kargs['priority'] = self.priority
        else:
            self.priority = kargs['priority']
        if 'confirm' not in kargs:
            kargs['confirm'] = 0
        kargs['sign'] = self.sign
        kargs['clientType'] = self.sdk_type
        kargs['cid'] = self.cid
        if kargs['confirm'] == 0:
            logger.info("cid-{cid}  request the instance".format(cid=self.cid))
        # get cloud service can get the default resolution if data have no key
        # if 'resolution' not in kargs: kargs['resolution'] = 1

        self.data = requests.generate_data_info(**kargs)
        params.data = self.data

        status, respone = self.__clould_request(params)
        res = json.loads(respone)
        self.__cloud_json_check(res)

    def stop_instance(self):
        params = requests.generate_comm_request(ACTION_STOP_CLOUD_SERVICE, self.sdk_type, self.protocol, self.did)
        params.data.sign = self.sign
        params.data.cid = self.cid
        try:
            if self.status  in [INSTANCE_IN_QUEUE, INSTANCE_SUCCESS_REQUEST, INSTANCE_DONE_REQUEST]:
                logger.info("cid-{cid}  stop the instance".format(cid=self.cid))
                status, respone = self.__clould_request(params)
                res = json.loads(respone)
                self.__cloud_json_check(res)
                self.status = USER_STOP
                for instance in self.cloud_user.instances:
                    if instance.cid == self.cid:
                        self.cloud_user.instances.remove(instance)
            if self.socket:
                self.socket.close()
            if self.countly:
                self.timer.cancel()
        except Exception as e:
            logger.exception("cid-%s Failed Action: stopInstance" %(self.cid))
            logger.exception(e.message)

    def notify_instance(self, status):
        if self.status == INSTANCE_DONE_REQUEST:
            logger.info("cid-{cid} Notify the instance with status {status}".format(cid=self.cid, status=status))
            params = requests.generate_comm_request(ACTION_PAAS_CALLBACK, self.sdk_type, self.protocol, self.did)
            instance_id = CloudDB().get_instance_id_by_cid(self.cid)
            params.data = requests.generate_instance_info(instance_id, status)
            status, respone = self.__clould_request(params)
            res = json.loads(respone)
            self.__cloud_json_check(res)
            for instance in self.cloud_user.instances:
                if instance.cid == self.cid:
                    self.cloud_user.instances.remove(instance)

    def refresh_stoken(self):
        params = requests.generate_comm_request(ACTION_GET_CLOUD_SERVICE, self.sdk_type, self.protocol, self.did)
        self.data.opType = 1
        params.data = self.data
        logger.info("cid-{cid}  Refresh the stoken".format(cid=self.cid))
        try:
            status, respone = self.__clould_request(params)
            res = json.loads(respone)
            self.__cloud_json_check(res)
        except Exception as e:
            logger.exception("cid-%s Action: refreshStoken" % (self.cid))
            logger.exception(e.message)

    def change_resolution(self, resolution="1"):
        params = requests.generate_comm_request(ACTION_GET_CLOUD_SERVICE, self.sdk_type, self.protocol, self.did)
        self.data.opType = 2
        self.data.resolution = resolution
        params.data = self.data
        logger.info("cid-{cid}  change the resolution".format(cid=self.cid))
        try:
            status, respone = self.__clould_request(params)
            res = json.loads(respone)
            self.__cloud_json_check(res)
        except Exception as e:
            logger.exception("cid-%s Failed Action: changeResolution" % (self.cid))
            logger.exception(e.message)

    def __create_connection(self, url):
        self.socket = create_connection(url)

    def websocket_connect(self, auto_confirm=True, ping=True):
        url = "%s/websocket?cid=%s&uid=%s&did=%s&appId=%s&sign=%s" \
              % (self.socket_url, self.cid, self.user_info['uid'], self.did, self.access_key, self.sign)
        t3 = threading.Thread(target=self.__create_connection, args=(url,))
        t3.setDaemon(False)
        t3.start()
        t3.join()

        t2 = threading.Thread(target=self.recv_data, args=(auto_confirm,))
        t2.setDaemon(False)
        if ping:
            t1 = threading.Thread(target=self.send_ping)
            t1.setDaemon(False)
            t1.start()
        t2.start()

    def send_ping(self):
        try:
            while True:
                self.socket.ping()
                time.sleep(5)
        except Exception:
            logger.warning("cid-%s websocket broke down; instance status: %s" % (self.cid, self.status))
        finally:
            self.socket.close()

    def recv_data(self, auto_confirm):
        try:
            while True:
                data = self.socket.recv()
                jsondata = json.loads(data)
                operation = json.loads(jsondata['payload'])['operation']
                self.messages.append(json.loads(jsondata['payload']))
                logger.debug(jsondata)
                if operation == 6:
                    logger.info("cid-{cid}  Waiting for the instance".format(cid=self.cid))
                    if auto_confirm:
                        self.get_instance(confirm=1)
                    self.status = INSTANCE_IN_QUEUE
                if operation == 10:
                    self.status = INSTANCE_SUCCESS_REQUEST
                    logger.info("cid-{cid}  recieve the instance ID".format(cid=self.cid))
                    pass
                if operation == 5:
                    self.status = INSTANCE_DONE_REQUEST
                    logger.info("cid-{cid}  recieve the instance Address".format(cid=self.cid))
                    if self.countly:
                        self.timer = threading.Timer(0, process_event, args=(self.cloud_countly, self,))
                        self.timer.start()
                if operation == 2:
                    logger.info("cid-{cid}  request is kicked".format(cid=self.cid))
                    self.status = INSTANCE_KICKED
                if operation == 3:
                    logger.info("cid-{cid}  instance broke down".format(cid=self.cid))
                    self.status = INSTANCE_SCRASH
                if operation == 4:
                    logger.info("cid-{cid}  playing time is over".format(cid=self.cid))
                    self.status = INSTANCE_OVERTIME
        except Exception:
            logger.warning("cid-%s websocket broke down; instance status: %s" % (self.cid, self.status))
        finally:
            self.socket.close()
            if self.countly and self.timer is not None:
                self.timer.cancel()

    def start_instance(self, **kargs):
        if 'confirm' in kargs:
            auto_confirm = kargs['confirm']
        else:
            auto_confirm = True

        if 'ping' in kargs:
            ping = kargs['ping']
        else:
            ping = True

        kargs['confirm'] = 0
        try:
            self.get_config()
            if self.countly:
                pre_events(self.cloud_countly, self)
            self.get_cid(kargs['pkgname'])
            self.websocket_connect(auto_confirm, ping)
            self.get_instance(**kargs)
        except Exception as e:
            logger.error("cid-%s Failed Action: startInstance" % (self.cid))
            logger.exception(e.message)

    def disconnected(self):
        self.socket.close()
