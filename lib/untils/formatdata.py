#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import random
import time

def random_int(start, end):
    return random.randint(start, end)


def random_str(randomlength=8, chars=None):
    tmp_str = ""
    if chars is None:
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for i in range(randomlength):
        tmp_str += chars[random.randint(0, length)]
    return tmp_str


def date_string():
    return repr(time.time()).replace(".", "")


def random_ip():
    return "222.222." + str(random_int(0, 255)) + "." + str(random_int(0, 255))

#50:7b:9d:a4:4d:39
def random_mac():
    tmp_mac = ""
    chars = "1234567890ABCDEF"
    for i in range(6):
        if i != 5:
            tmp_mac += random_str(2, chars)
            tmp_mac += ":"
        else:
            tmp_mac += random_str(2, chars)
    return  tmp_mac

def random_apn():
    return random.choice(["中国移动", "中国联通", "中国电信"])

def random_phone_num():
    return random_str(11, "1234567890")

#generate the imsi or imei
def random_im():
    return random_str(15, "1234567890")


def expand_int(num, leng=5):
    neednum = leng - len(str(num))
    return '0' * neednum + str(num)

if __name__ == "__main__":
    print random_mac()