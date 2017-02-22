#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from constants import *
from Crypto.Cipher import AES
import base64
from untils import formatdata
import json
import md5
import hashlib
import xtestlogger
from clouddb import CloudDB

logger = xtestlogger.get_logger(__name__)

def __encrypt(content, key):
    # iv = random_str(16)
    block_size = AES.block_size
    pad = lambda s: s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size)
    cryptor = AES.new(key)
    tmp_str = cryptor.encrypt(pad(content))
    return base64.b64encode(tmp_str)


def __decrypt(content, key):
    tmp_str = base64.b64decode(content)
    cryptor = AES.new(key)
    data = cryptor.decrypt(tmp_str)
    data = data[0:data.rindex('}') + 1]
    return data


def __get_encrypt_key(context, secret_key):
    action = context.action.actId
    sdk_type = int(context.action.sdkType)
    pre_key = None
    if action in [ACTION_GET_CLOUD_SERVICE, ACTION_STOP_CLOUD_SERVICE]:
        return secret_key
    else:
        if sdk_type == TYPE_ANDROID:
            pre_key = SECRET_KEY_ANDROID
        if sdk_type == TYPE_IOS:
            pre_key = SECRET_KEY_IOS
        if sdk_type == TYPE_WEB:
            pre_key = SECRET_KEY_WEB
        if sdk_type == TYPE_PC:
            pre_key = SECRET_KEY_PC
        if sdk_type == TYPE_MAC:
            pre_key = SECRET_KEY_MAC
        secret_key = pre_key + context.action.random
        return secret_key.lower()


def encrypt_cloud_request(context, secret_key):
    protocol_version = context.action.protocol.split(".")[0]
    action = context.action.actId
    if protocol_version >= "3" and action != ACTION_PAAS_CALLBACK:
        if action in [ACTION_GET_CLOUD_SERVICE, ACTION_STOP_CLOUD_SERVICE]:
            context.action.random = context.data.cid
        else:

            context.action.random = formatdata.random_str(16).lower()
        secret_key = __get_encrypt_key(context, secret_key)
        logger.debug("[request: %s]" % (context))
        context.data = __encrypt(json.dumps(context.data), secret_key)
        if hasattr(context, 'client'):
            context.client = __encrypt(json.dumps(context.client), secret_key)
        if hasattr(context, 'device'):
            context.device = __encrypt(json.dumps(context.device), secret_key)
    else:
        logger.debug("[request: %s]" % (context))
    return context


def decrypt_cloud_response(context, secret_key):
    protocol_version = context.action.protocol.split(".")[0]
    action = context.action.actId
    if protocol_version >= "3" and action != ACTION_PAAS_CALLBACK:
        secret_key = __get_encrypt_key(context, secret_key)
        context.data = __decrypt(json.dumps(context.data), secret_key)
        context.data = json.loads(context.data)
        if hasattr(context, 'client'):
            context.client = __decrypt(json.dumps(context.client), secret_key)
        if hasattr(context, 'device'):
            context.device = __decrypt(json.dumps(context.device), secret_key)

    logger.debug("[respones: %s]" % (context))
    return context

def generate_maintain_sign(op_type, start_time, end_time):
    secret = "541839238jdj0923441f43d7254a97579e7bcf"

    params = {}
    params['startTime'] = start_time
    params['endTime'] = end_time
    params['type'] = str(op_type)

    result = ""
    keys = params.keys()
    for key in sorted(keys):
        if key.lower() != "sign":
            result = result + key + "=" + params[key] + "&"

    result = result + "key=" + secret + secret
    m1 = md5.new()
    m1.update(bytes(result))
    #hashlib.md5(data)
    return m1.hexdigest()


def hexstring_2_byte(key):
    max = len(key)/2
    result = ""
    for i in range(max):
        result +=  chr(int(key[i*2:i*2+2], 16) & 0xff)

    return result

def generate_ctoken(context):
    key_db = CloudDB()
    key = key_db.get_key(context.client.accessKeyID)
    raw = context.data.userInfo.uid + context.data.userInfo.uToken + context.data.pkgName + context.client.accessKeyID + str(
        context.client.channel)
    block_size = AES.block_size
    pad = lambda s: s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size)
    cryptor = AES.new(hexstring_2_byte(key))
    tmp_str = cryptor.encrypt(pad(raw))
    test = hashlib.sha1(bytes(tmp_str))
    return test.hexdigest()

if __name__ == "__main__":
    key = "5372185a0b276e0842e64eec928172d8"
    print hexstring_2_byte(key)
