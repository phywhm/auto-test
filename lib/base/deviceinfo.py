#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from baseinfo import BaseInfo

class AndriodInfo(BaseInfo):
    def __init__(self):
        super(AndriodInfo, self).__init__()
        self.__attrs__ = ['androidId', 'macAddress', 'bluetoothMac', 'apn', 'phonenum']


class IOSInfo(BaseInfo):
    def __init__(self):
        super(IOSInfo, self).__init__()
        self.__attrs__ = ['udid', 'openUdid', 'idfa', 'idfv', 'iosModle', 'iosSysType', 'certificateType', 'apn']


class PcInfo(BaseInfo):
    def __init__(self):
        super(PcInfo, self).__init__()
        self.__attrs__ = ['pcDid', 'cpuType', 'memorySize', 'hardDiskId', 'macAddress', 'openVtYN', 'graphics']


class WebInfo(BaseInfo):
    def __init__(self):
        super(WebInfo, self).__init__()
        self.__attrs__ = ['userAgent', 'platform', 'browserType', 'installLocSignYN', 'cookieId']


class MacInfo(BaseInfo):
    def __init__(self):
        super(MacInfo, self).__init__()
        self.__attrs__ = ['macDid', 'cpuType', 'memorySize', 'hardDiskId', 'macAddress']


class ScreenInfo(BaseInfo):
    def __init__(self):
        super(ScreenInfo, self).__init__()
        self.__attrs__ = ['dpi', 'resolution']


class DeviceInfo(BaseInfo):
    def __init__(self):
        super(DeviceInfo, self).__init__()
        self.__attrs__ = ['ip', 'mac', 'imei', 'imsi', 'osType', 'osVersion', 'brand', 'model', 'isWifi', 'networkType',
                 'dataCenterId', 'androidInfo', 'iosInfo', 'pcInfo', 'webInfo', 'macInfo', 'screenInfo']


if __name__ == "__main__":
    test = DeviceInfo()
    test.mac = "test"
    print(test.mac)
    print(test)
