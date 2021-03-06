#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import os
import ConfigParser


def load_config_file():
    ''' Load Config File order(first found is used): ENV, CWD, HOME '''

    p = ConfigParser.ConfigParser()

    path0 = os.getenv("CLOUD_RUN_CONFIG", None)
    if path0 is not None:
        path0 = os.path.expanduser(path0)
        if os.path.isdir(path0):
            path0 += "/cloudrun.cfg"
    try:
        path1 = os.getcwd() + "/cloudrun.cfg"
    except OSError:
        path1 = None
    path2 = os.path.expanduser("~/.cloudrun.cfg")

    for path in [path0, path1, path2]:
        if path is not None and os.path.exists(path):
            try:
                p.read(path)
            except:
                print("error  configparser ")
            return p
    return None


def _get_config(p, section, key, env_var, default):
    ''' helper function for get_config '''
    if env_var is not None:
        value = os.environ.get(env_var, None)
        if value is not None:
            return value
    if p is not None:
        try:
            return p.get(section, key, raw=True)
        except:
            return default
    return default


p = load_config_file()
# SAAS_HOST = _get_config(p, "cloudenv", 'saas_host', "SAAS_HOST", "172.16.2.125")       #测试环境
SAAS_HOST = _get_config(p, "cloudenv", 'saas_host', "SAAS_HOST", "docker-mgt.haima.me")       #开发环境
#SAAS_HOST = _get_config(p, "cloudenv", 'saas_host', "SAAS_HOST", "172.16.2.100")        #demo
#SAAS_HOST = _get_config(p, "cloudenv", 'saas_host', "SAAS_HOST", "172.16.2.169")    #支付
#SAAS_HOST = _get_config(p, "cloudenv", 'saas_host', "SAAS_HOST", "saasauth-migu# .haimawan.com")  #teng saas
#SAAS_HOST = "saasAuth-pre.haimawan.com"
# SAAS_PORT = _get_config(p, "cloudenv", 'saas_port', "SAAS_PORT", "8010")
SAAS_PORT = _get_config(p, "cloudenv", 'saas_port', "SAAS_PORT", "8070")



DB_HOST = _get_config(p, "cloudenv", 'db_host', "DB_HOST", "docker-mgt.haima.me")  #开发环境
DB_PORT = _get_config(p, "cloudenv", 'db_port', "DB_PORT", 3306)
DB_USER = _get_config(p, "cloudenv", 'db_user', "DB_USER", "admin")
DB_PASSWD = _get_config(p, "cloudenv", 'db_passwd', "DB_PASSWD", "123qwe")
TENANT_DB = _get_config(p, "cloudenv", 'tenant_db', "TENANT_DB", 'db_tenant_mgt')
CORE_DB = _get_config(p, "cloudenv", 'tenant_db', "CORE_DB", 'db_service_core')
MC_DB = _get_config(p, "cloudenv", 'msg_center_db', "MC_DB", 'db_msg_center')


#
# AMQP_USER = _get_config(p, 'cloudenv', 'amqp_user', "AMQP_USER", "admin")
# AMQP_PASSWD = _get_config(p, 'cloudenv', 'amqp_passwd', "AMQP_PASSWD", "admin")
# AMQP_HOST = _get_config(p, 'cloudenv', 'amqp_host', "AMQP_HOST", "docker-mgt.haima.me")
# AMQP_PORT = _get_config(p, 'cloudenv', 'amqp_port', "AMQP_PORT", 5672)
# VIRTUAL_HOST = _get_config(p, 'cloudenv', 'virtual_host', "VIRTUAL_HOST", "/")
AMQP_USER = _get_config(p, 'cloudenv', 'amqp_user', "AMQP_USER", "admin")
AMQP_PASSWD = _get_config(p, 'cloudenv', 'amqp_passwd', "AMQP_PASSWD", "HaimaRabbBit81")
AMQP_HOST = _get_config(p, 'cloudenv', 'amqp_host', "AMQP_HOST", "service-core.stable.haima001.com")
AMQP_PORT = _get_config(p, 'cloudenv', 'amqp_port', "AMQP_PORT", 5672)
VIRTUAL_HOST = _get_config(p, 'cloudenv', 'virtual_host', "VIRTUAL_HOST", "fc")


REDIS_HOST = _get_config(p, 'cloudenv', 'redis_host', "REDIS_HOST", "123.206.46.217")
# REDIS_HOST = _get_config(p, 'cloudenv', 'redis_host', "REDIS_HOST", "docker-mgt.haima.me")
REDIS_PORT = _get_config(p, 'cloudenv', 'redis_port', "REDIS_PORT", 6379)
REDIS_DB = _get_config(p, 'cloudenv', 'redis_db', "REDIS_DB", 0)
# REDIS_DB = _get_config(p, 'cloudenv', 'redis_db', "REDIS_DB", 0)
REDIS_PASSWD = _get_config(p, 'cloudenv', 'redis_passwd', "REDIS_PASSWD", "redispass")
# REDIS_PASSWD = _get_config(p, 'cloudenv', 'redis_passwd', "REDIS_PASSWD", "123qwe")

MONGO_HOST = _get_config(p, 'cloudenv', 'redis_host', "REDIS_HOST", "172.16.2.16")
MONGO_PORT = _get_config(p, 'cloudenv', 'redis_port', "REDIS_PORT", 27017)
CONFIG_DB = _get_config(p, 'cloudenv', 'config_db', "CONFIG_DB", 'db_tenant_test')
MONGO_USER = _get_config(p, 'cloudenv', 'mongo_user', "MONGO_USER", "admin")
MONGO_PASSWORD = _get_config(p, 'cloudenv', 'mongo_password', "MONGO_PASSWORD", "123qwe")



USE_CTOKEN_BACKDOOR = _get_config(p, 'cloudenv', 'use_ctoken_backdoor', "USE_CTOKEN_BACKDOOR", 1)
PROTOCOL_VERSION = _get_config(p, 'cloudenv', 'protocol_version', "PROTOCOL_VERSION", "1.1")

MOCK_SERVER = _get_config(p, "cloudenv", 'mock_server', "MOCK_SERVER", "127.0.0.1")
MOCK_PORT = _get_config(p, "cloudenv", 'mock_port', "MOCK_PORT", "8080")
SECRET_KEY = _get_config(p, 'cloudenv', 'secret_key', 'SECRET_KEY', 'and0123456789012')
PASS_DB = _get_config(p, "cloudenv", 'paas_db', "PASS_DB", "cloudplayer_controller_show")
