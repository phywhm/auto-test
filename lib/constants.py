#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
__两个下划线表示私有
_一个下划线表示保护, import的是不会被导入
"""
class _const:
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, key, value):
        if self.__dict__.has_key(key):
            raise self.ConstError, "Can not change const.{0}".format(key)
        if not key.isupper():
            raise  self.ConstCaseError, "const name {0} is not all upper".format(key)
        self.__dict__[key] = value

import sys
sys.modules['const'] = _const()
import const


const.TEST = 2
TYPE_WEB = 3
TYPE_ANDROID = 2
TYPE_IOS = 4
TYPE_PC = 1
TYPE_MAC = 5


ACTION_CID = 102
ACTION_DID_REGISTER = 104
ACTION_REGISTER_MSG = 106
ACTION_UPDATE_CID_STATUS = 107
ACTION_GET_CONFIGURE = 108
ACTION_GET_CLOUD_SERVICE = 201
ACTION_STOP_CLOUD_SERVICE = 202
ACTION_PAAS_CALLBACK = 203
ACTION_STOP_SAAS = 301


SECRET_KEY_ANDROID = "and0123456789012"
SECRET_KEY_IOS = "ios0123456789012"
SECRET_KEY_PC = "pc01234567890123"
SECRET_KEY_MAC = "mac0123456789012"
SECRET_KEY_WEB = "web0123456789012"

INSTANCE_NOT_REQUEST = -1
INSTANCE_SUCCESS_REQUEST = 0
INSTANCE_IN_QUEUE = 1
INSTANCE_DONE_REQUEST = 2
INSTANCE_KICKED = 3
INSTANCE_OVERTIME = 4
INSTANCE_SCRASH = 5
INSTANCE_RELEASE = 6
USER_STOP = 7

DEFAULT_ACCESS_KEY = "9599e53c"


TOTAL_WAIT_USER_DATA_KEY = "countly_total_user_wait_data"
TOTAL_WAIT_TIME_KEY = "totalWaitTime"
TOTAL_WAIT_USERS_KEY = "totalWaitUsers"
AVG_WAIT_TIME_KEY = "avgWaitTIme"

REDIS_CLIENT_ROUTE_PREFIX = "mc_clb_"