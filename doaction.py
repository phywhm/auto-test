#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import os
import sys
import ConfigParser
import argparse
from lib.clouduser import CloudUser
from lib.cloud_amqp import CloudAMQP
import time
from lib import cloud_tools
from lib.constants import *


def load_env(env):
    config_path = os.path.join(sys.path[0], "etc/env.cfg")
    config = ConfigParser.ConfigParser()
    config.read(config_path)

    os.environ["SAAS_HOST"] = config.get(env, 'saas_host')
    os.environ["SAAS_PORT"] = config.get(env, 'saas_port')
    os.environ["DB_HOST"] = config.get(env, 'db_host')
    os.environ["DB_PORT"] = config.get(env, 'db_port')
    os.environ["DB_USER"] = config.get(env, 'db_user')
    os.environ["DB_PASSWD"] = config.get(env, 'db_passwd')



def start_instance(args):
    cloud_user = CloudUser(args.user, args.passwd)
    inst = cloud_user.start_instance(args.package, playingTime=args.playtime)
    for x in range(args.playtime):
        time.sleep(1)
        if inst.status in [INSTANCE_NOT_REQUEST, INSTANCE_KICKED, INSTANCE_SCRASH]:
            break
    cloud_user.stop_instances()


def notify_message(args):
    virtual_client = CloudAMQP()
    if args.type == "waiting":
        virtual_client.send_wait_message(args.cid)
    elif args.type == "refuse":
        virtual_client.send_refuse_message(args.cid)
    elif args.type == "confirm":
        virtual_client.send_choose_message(args.cid)
    elif args.type == "error":
        virtual_client.send_error_message(args.cid)
    elif args.type == "kicked":
        virtual_client.send_kicked_message(args.cid)
    elif args.type == "overtime":
        virtual_client.send_overtime_message(args.cid)
    elif args.type == "overtime":
        virtual_client.send_overtime_message(args.cid)
    else:
        pass


def maintain_server(args):
    if args.type == "stop":
        cloud_tools.stop_service(args.start_time, args.end_time)
    else:
        cloud_tools.recover_server()


lib_path = os.path.join(sys.path[0], "../lib")
sys.path.append(lib_path)







parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="""run the parallel request from cmd
    e.g
    ./doaction.py -e pay
    you can specify params as your want""")

parser.add_argument('-e', '--env', required=True, help="specify the env you want to operation on")
subparser = parser.add_subparsers(title="action",
                      description="specify the action you want to do")

create_instance = subparser.add_parser('start_instance', help="start instance in the env you specified")
create_instance.add_argument('-u', '--user', default='xxtester', help="specify the user")
create_instance.add_argument('-p', '--passwd',default='xxtester', help="specify the utoken of user")
create_instance.add_argument('-P', '--package', required=True, help="specify the package name")
create_instance.add_argument('-t', '--playtime', type=int, default=60, help="specify the time you want you play")
create_instance.set_defaults(do=start_instance)

send_message = subparser.add_parser("send_message", help="send mesage to SDK")
send_message.add_argument('-t', '--type', choices=['te', '2'], required=True, help="specify the message type")
send_message.add_argument('-c', '--cid', required=True, help="specify the cid you want to send to")
send_message.set_defaults(do=notify_message)


send_message = subparser.add_parser("maintain", help="send mesage to SDK")
send_message.add_argument('-t', '--type', choices=['stop', 'resume'], required=True, help="specify the message type")
send_message.add_argument('-s', '--start_time', required=True, help="specify the cid you want to send to")
send_message.add_argument('-e', '--end_time', required=True, help="specify the cid you want to send to")
send_message.set_defaults(do=maintain_server)

args = parser.parse_args()

load_env(args.env)
args.do(args)