#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from baseinfo import BaseInfo


class ClientInfo(BaseInfo):
    def __init__(self):
        super(ClientInfo, self).__init__()
        self.__attrs__ = ['accessKeyID', 'clientPkgName', 'sdkVersion', 'channel']