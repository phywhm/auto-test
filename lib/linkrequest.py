#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import threading
import time

from websocket import WebSocketTimeoutException, WebSocketConnectionClosedException
from websocket import create_connection

import xtestlogger
from constants import *

logger = xtestlogger.get_logger("link")


class WebSocketException(Exception):
    def __init__(self, msg):
        self.message = msg


class CloudStatus(object):
    __slots__ = ['success', 'waiting', 'instance', 'release', 'status']

    def __init__(self):
        self.success = True
        self.waiting = False
        self.instance = False
        self.release = None
        self.status = INSTANCE_SUCCESS_REQUEST


class LinkRequest(object):
    def __init__(self, cid, ctx):
        self.did = None
        self.cid = cid
        self.sign = None
        self.socket = None
        self.ctx = ctx
        self.cloud_status = CloudStatus()

    def __create_connection(self, url):
        self.socket = create_connection(url)
        self.socket.settimeout(5)

    def websocket_connect(self, auto_confirm=True, ping=True):
        url = "ws://docker-mgt.haima.me:7099/websocket?cid=%s&uid=%s&did=%s&sign=%s" \
              % (self.cid, 'testuidp', self.did, self.sign)
        t3 = threading.Thread(target=self.__create_connection, args=(url,))
        t3.setDaemon(False)
        t3.start()
        t3.join()
        t2 = threading.Thread(target=self.recv_data, args=(ping,))
        t2.setDaemon(False)
        t2.start()

    def send_ping(self):
        try:
            i = 0
            while self.socket is not None:
                i += 1
                if i < 20:
                    time.sleep(1)
                else:
                    i = 0
                    self.socket.ping()
        except Exception as e:
            logger.warning("cid-%s websocket broke down; instance status: %s ,caused by %s" % (self.cid, self.cloud_status.status, e.message))
        finally:
            if self.socket:
                self.socket.close()

    def recv_data(self, ping):
        try:
            i = 0
            while self.socket is not None:
                i += 1
                if i == 15:
                    i = 0
                    if ping:
                        self.socket.ping()
                try:
                    data = self.socket.recv()
                    self.ctx.recv[self.cid].append(data)
                except WebSocketTimeoutException:
                    continue
                logger.info("cid-{cid} {data}".format(cid=self.cid, data=data))
                time.sleep(0.1)
        except WebSocketConnectionClosedException as e:
            logger.warning("cid-%s websocket disconnect from server; instance status: %s" % (self.cid, self.cloud_status.status))
        except Exception as e:
            pass
            # logger.exception(e.message)
        finally:
            logger.warning("cid-%s intance-status  %-15s%-15s%-15s%-15s" % (
                self.cid, self.cloud_status.success, self.cloud_status.waiting, self.cloud_status.instance,
                self.cloud_status.release))
            if self.socket:
                self.socket.close()

    def disconnected(self):
        if self.socket:
            self.socket.close()
        else:
            logger.info("socket already closed")

