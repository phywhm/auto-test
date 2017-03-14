#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time
from encryption import generate_maintain_sign
import configuration as CONFIG




def stop_service(start_time, end_time):
    reload(CONFIG)
    timeArray = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    start_time = str(int(time.mktime(timeArray)) * 1000)

    timeArray = time.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    end_time = str(int(time.mktime(timeArray)) * 1000)

    sign = generate_maintain_sign(1, start_time, end_time)

    post_data = copy.deepcopy(STOP_SERVICE)

    post_data['data']['type'] = 1
    post_data['data']['startTime'] = start_time
    post_data['data']['endTime'] = end_time
    post_data['data']['sign'] = sign
    run_request("http://" + CONFIG.SAAS_HOST + ":" + CONFIG.SAAS_PORT + "/s/rest/api", "POST", post_data)


def recover_server():
    reload(CONFIG)
    start_time = end_time = "2017-10-11 20:23:00"
    timeArray = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    start_time = str(int(time.mktime(timeArray)) * 1000)

    timeArray = time.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    end_time = str(int(time.mktime(timeArray)) * 1000)

    sign = generate_maintain_sign(2, start_time, end_time)

    post_data = copy.deepcopy(STOP_SERVICE)

    post_data['data']['type'] = 2
    post_data['data']['startTime'] = start_time
    post_data['data']['endTime'] = end_time
    post_data['data']['sign'] = sign
    run_request("http://" + CONFIG.SAAS_HOST + ":" + CONFIG.SAAS_PORT + "/s/rest/api", "POST", post_data)