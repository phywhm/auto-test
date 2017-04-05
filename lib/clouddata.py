#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from base import *
from untils import formatdata
from constants import *


def generate_android_info():
    android_info = AndriodInfo()
    android_info.androidId = "Test android" + formatdata.random_str(5)
    android_info.macAddress = formatdata.random_mac()
    android_info.bluetoothMac = formatdata.random_mac()
    android_info.apn = formatdata.random_apn()
    android_info.phonenum = formatdata.random_phone_num()
    return android_info


def generate_ios_info():
    ios_info = IOSInfo()
    ios_info.udid = "test IOS" + formatdata.random_str(5)
    ios_info.openUdid = "test" + formatdata.random_str(6)
    ios_info.idfa = "test" + formatdata.random_str(5)
    ios_info.idfv = "test" + formatdata.random_str(5)
    ios_info.apn = formatdata.random_apn()
    return ios_info


def generate_pc_info():
    pc_info = PcInfo()
    pc_info.pcDid = "test" + formatdata.random_str(5)
    pc_info.macAddress = formatdata.random_mac()
    pc_info.cpuType = "xxIntel MX"
    pc_info.memorySize = "100G"
    pc_info.hardDiskId = formatdata.random_str(32)
    pc_info.macAddress = formatdata.random_mac()
    pc_info.graphics = "xxGTX750Ti"
    return pc_info


def generate_web_info():
    web_info = WebInfo()
    web_info.browserType = "Test Inc"
    web_info.platform = "Test Linux"
    web_info.userAgent = "Test Web" + formatdata.random_str(10)
    return web_info


def generate_mac_info():
    mac_info = MacInfo()
    mac_info.macDid = "Test Mac" + formatdata.random_str(5)
    mac_info.macAddress = formatdata.random_mac()
    return mac_info


def generate_screen_info():
    screen_info = ScreenInfo()
    screen_info.dpi = formatdata.random_int(300, 400)
    screen_info.resolution = "1297x999"
    return screen_info


def generate_action_info(action_type, sdk_type, protocol, did):
    action = ActionInfo()
    action.transId = formatdata.date_string()
    # no encrypt by default
    if protocol is not None:
        action.protocol = protocol
    action.actId = action_type
    if sdk_type is not None:
        action.sdkType = sdk_type
    if did is not None:
        action.did = did
    return action


def generate_client_info():
    client_info = ClientInfo()
    client_info.sdkVersion = "2.2.test"
    client_info.channel = '00000222222222'
    client_info.accessKeyID = DEFAULT_ACCESS_KEY
    return client_info


def generate_device_info(sdk_type, client_ip=None):
    device_info = DeviceInfo()
    if client_ip:
        device_info.ip = client_ip
    else:
        device_info.ip = formatdata.random_ip()
    if sdk_type == TYPE_WEB:
        device_info.webInfo = generate_web_info()
        device_info.screenInfo = generate_screen_info()
        device_info.networkType = ""
        device_info.isWifi = ""
        device_info.hardDecoderSupported = "1"
    if sdk_type == TYPE_ANDROID:
        device_info.androidInfo = generate_android_info()
        device_info.screenInfo = generate_screen_info()
        device_info.imei = formatdata.random_im()
        device_info.imsi = formatdata.random_im()
        device_info.brand = "xxTest"
        device_info.networkType = "wifi"
        device_info.isWifi = 1
        device_info.osVersion = "2.2." + str(formatdata.random_int(10, 99))
    if sdk_type == TYPE_IOS:
        device_info.iosInfo = generate_ios_info()
        device_info.model = "Iphone6"
        device_info.networkType = "wifi"
        device_info.isWifi = 1
    if sdk_type == TYPE_PC:
        device_info.pcInfo = generate_pc_info()
        device_info.networkType = ""
        device_info.isWifi = ""
    if sdk_type == TYPE_MAC:
        device_info.macInfo = generate_mac_info()
    return device_info


def generate_comm_request(action_type, sdk_type=None, protocol=None, did=None):
    comm_request = CommAction()
    comm_request.action = generate_action_info(action_type, sdk_type, protocol, did)
    comm_request.data = BaseInfo()
    return comm_request


def generate_data_info(**kargs):
    data_info = BaseInfo()
    for key, value in kargs.items():
        if key in ['cid', 'sign', 'clientType', 'resolution', 'opType', 'clientType', 'playingTime', 'priority', 'confirm']:
            setattr(data_info, key, value)

    return data_info
def generate_instance_info(instance_id, status):
    data_info = BaseInfo()
    instance_info = BaseInfo()
    data_info.notifyType = "1"
    if status in ["01", "23", "31"]:
        instance_info.serviceId = instance_id
        instance_info.status = status
        data_info.sToken = formatdata.random_str(64)

        ip = "192.168.%s.%s" % (formatdata.random_int(0, 249), formatdata.random_int(0, 249))
        audio = "rtmp://%s1935/publishlive/mystreamaudio?st=%s" % (ip, data_info.sToken)
        video = "rtmp://%s1935/publishlive/mystream?st=%s" % (ip, data_info.sToken)
        url = "ws://%s:7681/%s" % (ip, data_info.sToken)


        stream_info = BaseInfo()
        stream_info.audioUrl = audio
        stream_info.videoUrl = video
        input_info = BaseInfo()
        input_info.url = url
        instance_info.streamInfo = stream_info
        instance_info.inputInfo = input_info
        data_info.InstanceInfo = instance_info
    else:
        instance_info.serviceId = instance_id
        instance_info.status = status
        data_info.InstanceInfo = instance_info

    return data_info




def convert_dict(data):
    for key in data.keys():
        if isinstance(data[key], dict):
            data[key] = convert_dict(data[key])
    return BaseInfo(data)

if __name__ == "__main__":
    pass
