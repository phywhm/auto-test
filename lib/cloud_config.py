#!/usr/bin/env python
# -*- coding: UTF-8 -*-


def get_value_from_key(cloud_config, child_config, key):
    for item in cloud_config[child_config]:
        if item['k'] == key:
            return item['v']
    return None

def get_value_from_name(cloud_config, child_config, name):
    for item in cloud_config[child_config]:
        if item['name'] == name:
            return item['enable']
    return None

def get_ctoken_backdoor(cloud_config):
    get_value_from_key(cloud_config, 'setDataInfo', 'ctoken_status_flag')
