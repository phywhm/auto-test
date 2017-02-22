#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from base.baseinfo import BaseInfo
import urllib
import urllib2
import random
import time
from constants import *




class CountlyEvent(BaseInfo):
    def __init__(self, key, event_segm):
        super(CountlyEvent, self).__init__()
        self.__attrs__ = ['key', 'count', 'segmentation', 'timestamp', 'hour', 'dow']
        if event_segm.key == TYPE_ANDROID:
            key = "HMCPAndroidEvent"
        if event_segm.key == TYPE_IOS:
            key = "HMCPiosEvent"
        if event_segm.key == TYPE_WEB:
            key = "HMCPWebEvent"
        if event_segm.key == TYPE_PC:
            key = "HMCPcpEvent"
        if event_segm.key == TYPE_MAC:
            key = "HMCPmacEvent"

        self.count = 1
        self.hour = 14
        self.dow = 5
        self.key = key
        self.segmentation = event_segm
        self.timestamp = event_segm.timeStamp



class EventSegm(BaseInfo):
    def __init__(self):
        super(EventSegm, self).__init__()
        self.__attrs__ = ['key', 'timeStamp', 'deviceID', 'eventID', 'cloudID', 'channel', 'extraId', 'eventData', 'uid', 'accessKeyId']



def new(cloud_request, event_id, event_data):

    segm = EventSegm()
    if cloud_request.cid is None:
        segm.cloudID = ""
    else:
        segm.cloudID = cloud_request.cid

    if event_data is None:
        event_data = ""

    segm.key = cloud_request.sdk_type
    segm.timeStamp = int(time.time()*1000)
    segm.deviceID = cloud_request.did
    segm.eventID = event_id

    segm.channel = cloud_request.client.channel
    segm.extraId = cloud_request.extra_id
    segm.eventData = event_data
    segm.uid = cloud_request.user_info.uid
    segm.accessKeyId = cloud_request.access_key
    return CountlyEvent(cloud_request.sdk_type, segm)



class CloudCountly():
    def __init__(self, host, app_key,device_id, sdk_type):
        if sdk_type == TYPE_ANDROID:
            self.sdk_name = "native_android"
        if sdk_type == TYPE_IOS:
            self.sdk_name = "native_ios"
        if sdk_type == TYPE_WEB:
            self.sdk_name = "native_web"
        if sdk_type == TYPE_PC:
            self.sdk_name = "native_pc"
        if sdk_type == TYPE_MAC:
            self.sdk_name = "native_mac"
        self.host = host
        self.app_key = app_key
        self.device_id = device_id
        self.timestamp = None
        self.events = []
        self.dow = 5
        self.hour = 14


    def append(self, cloud_event):
        timestamp = cloud_event.timestamp / 1000
        if self.timestamp is None:
            self.events.append(cloud_event)
            self.timestamp = timestamp
        else:
            if self.timestamp == timestamp:
                self.events.append(cloud_event)
            else:
                self.post_events()
                self.timestamp = timestamp
                self.events.append(cloud_event)


        time.sleep(random.randint(200, 1000)/1000)

    def post_events(self):
        host = self.host + "/i?" + self.post_params()
        req = urllib2.Request(host)
        res_data = urllib2.urlopen(req)
        print res_data.read()
        self.timestamp = None
        self.events = []



    def post_params(self):
        params2 = {}
        params = ""
        for key in ['app_key', 'device_id', 'dow', 'events', 'hour', 'sdk_name', 'timestamp']:
            if key == 'events':
                self.events = urllib.quote(str(self.events).replace("'", '"'))
            params2[key] = getattr(self, key)
            if params == "":
                params += "{key}={value}".format(key=key, value=getattr(self, key))
            else:
                params += "&{key}={value}".format(key=key, value=getattr(self, key))
        return params




def __get_do(percent):
    """
    return True or false according to the percent
    :param percent: percent is the '10' of '10%', such as: 0.1, 0.01
    :return: True or False
    """
    num = random.randint(0, 9999)
    if num in range(0, int(percent*100)):
        return True
    else:
        return False




def pre_events(cloud_countly, cloud_request):
    #12024  片头预加载开始
    cloud_event = new(cloud_request, 12024, None)
    cloud_countly.append(cloud_event)
    if __get_do(99.5):
        #12025 片头预加载成功
        cloud_event = new(cloud_request, 12025, None)
        cloud_countly.append(cloud_event)
        #12027 开始播放片头
        cloud_event = new(cloud_request, 12027, None)
        cloud_countly.append(cloud_event)
        if __get_do(99.5):
            # 12028 播放片头成功
            cloud_event = new(cloud_request, 12028, None)
            cloud_countly.append(cloud_event)
        else:
            # 12029 播放片头失败
            cloud_event = new(cloud_request, 12029, None)
            cloud_countly.append(cloud_event)
    else:
        # 12025 片头预加载失败
        cloud_event = new(cloud_request, 12026, None)
        cloud_countly.append(cloud_event)
    # 10012 开始云玩儿事件
    cloud_event = new(cloud_request, 10012, None)
    cloud_countly.append(cloud_event)


# 测速的时候, 请求已经获取到cid.
def after_events(cloud_countly, cloud_request):
    #12030 开始测速
    cloud_event = new(cloud_request, 12030, None)
    cloud_countly.append(cloud_event)
    if __get_do(99.5):
        # 12031 测速成功
        cloud_event = new(cloud_request, 12031, "2388176.8")
    else:
        # 12032 测速失败
        cloud_event = new(cloud_request, 12032, None)
    cloud_countly.append(cloud_event)


    #TODO: 这部分产品没有定义好
'''
    if __get_do(99.5):
        # 12020 菊花加载成功
        cloud_event = new(cloud_request, 12020, None)
    else:
        # 12021 菊花加载失败
        cloud_event = new(cloud_request, 12021, None)
    cloud_countly.append(cloud_event)

    if __get_do(99.5):
        # 12022 预加载背景图成功
        cloud_event = new(cloud_request, 12022, None)
    else:
        #  12023 预加载背景图失败
        cloud_event = new(cloud_request, 12023, None)
    cloud_countly.append(cloud_event)
'''

def process_event(cloud_countly, cloud_request):
    # 12039 播流启动时,当前码率上报
    # TODO: 缺少事件数据, 码率id:码率
    cloud_event = new(cloud_request, 12039, None)
    cloud_countly.append(cloud_event)

    # 12040 播流应用进入前台
    cloud_event = new(cloud_request, 12040, None)
    cloud_countly.append(cloud_event)


    if __get_do(99.8):
        # 12033 音频流链接成功
        #  12034 视频流链接成功
        cloud_event = new(cloud_request, 12033, None)
        cloud_countly.append(cloud_event)
        cloud_event = new(cloud_request, 12034, None)
        cloud_countly.append(cloud_event)
    else:
        # 12035 音频流链接失败
        # 12036 视频流链接失败
        cloud_event = new(cloud_request, 12035, None)
        cloud_countly.append(cloud_event)
        cloud_event = new(cloud_request, 12036, None)
        cloud_countly.append(cloud_event)

    if cloud_request.sdk_type in [TYPE_MAC, TYPE_PC, TYPE_WEB]:
        if __get_do(90):
            #12001 用户点击全屏
            cloud_event = new(cloud_request, 12001, None)
            cloud_countly.append(cloud_event)
            if __get_do(60):
                # 12001 用户退出全屏
                cloud_event = new(cloud_request, 12002, None)
                cloud_countly.append(cloud_event)


    if cloud_request.playing_time <= 300000:
        max_limit = cloud_request.playing_time
    else:
        max_limit = 300000
    intervals = []
    for i in range(6):
        intervals.append(random.randint(0, max_limit))
        intervals = sorted(intervals)


    for i in range(len(intervals)):
        if i == 0:
            time.sleep(intervals[i]/1000)
            # 12005 开始键位； 12006 点击预设键位； 12007 自定义预设键位; 12009  保存预设键位; 12004 关闭键位
            if __get_do(90):
                for key in [12005, 12006, 12007, 12009, 12004]:
                    cloud_event = new(cloud_request, key, None)
                    cloud_countly.append(cloud_event)
        else:
            time.sleep((intervals[i] - intervals[i-1])/1000)
            if i == 1 or i == 3:
                if __get_do(90):
                    change_resolution(cloud_countly, cloud_request)
            elif i == 2:
                if __get_do(30):
                    # 12017 检测到wifi进入移动网络环境
                    cloud_event = new(cloud_request, 12017, 4)
                    cloud_countly.append(cloud_event)
            elif i == 4:
                if __get_do(30):
                    # 12017 检测到wifi进入移动网络环境
                    cloud_event = new(cloud_request, 12017, 4)
                    cloud_countly.append(cloud_event)
            else:
                if __get_do(90):
                    change_resolution(cloud_countly, cloud_request, False)




def change_resolution(cloud_countly, cloud_request, auto=True):
    resolutions = {'4': '6400000', '3': '4800000', '2': '3200000', '1': '1600000'}
    change_from = str(random.randint(3, 4))
    change_to = str(random.randint(1, 2))
    change_time = str(random.randint(400, 1200))

    change_str = "{change_from}:{from_resolution},{change_to}:{to_resolution}".format(change_from=change_from,
                                                                                      from_resolution=resolutions[
                                                                                          change_from],
                                                                                      change_to=change_to,
                                                                                      to_resolution=resolutions[
                                                                                          change_to])

    success_str = "{from_resolution}:{from_resolution},{from_resolution}:{from_resolution}".format(change_from=change_from,
                                                                                      from_resolution=resolutions[
                                                                                          change_from])

    if auto:
        # 12010 触发切换场景
        cloud_event = new(cloud_request, 12010, change_from)
        cloud_countly.append(cloud_event)
        # 12011 开始自动切换
        cloud_event = new(cloud_request, 12011, change_str + ",10,60,50,30")
        cloud_countly.append(cloud_event)
        # 12012 自动切换成功
        cloud_event = new(cloud_request, 12012, success_str + "," + change_time)
        cloud_countly.append(cloud_event)
    else:
        # 12014 开始自动切换
        cloud_event = new(cloud_request, 12014, change_str + ",10,60,50,30")
        cloud_countly.append(cloud_event)
        # 12015 自动切换成功
        cloud_event = new(cloud_request, 12015, success_str + "," + change_time)
        cloud_countly.append(cloud_event)



if __name__ == "__main__":
    print __get_do(100)
