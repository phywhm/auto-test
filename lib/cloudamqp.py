#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import random

import pika
import configuration as CONFIG
from base.cloud_message import CloudMessage
from lib.base.msg_carrier import SingleMsg, GroupMsg, KickClient, AllocGroup


class CloudAMQP(object):
    def __init__(self, host=None, port=5672, virtual_host="/", password="admin"):
        if host:
            credential = pika.PlainCredentials("admin", password)
            self.amqp_params = pika.ConnectionParameters(host=host, port=port, virtual_host=virtual_host,
                                                         credentials=credential)
        else:
            credential = pika.PlainCredentials(CONFIG.AMQP_USER, CONFIG.AMQP_PASSWD)
            self.amqp_params = pika.ConnectionParameters(host=CONFIG.AMQP_HOST, port=CONFIG.AMQP_PORT, virtual_host=CONFIG.VIRTUAL_HOST,
                                                         credentials=credential)

        self.amqp_conn = pika.BlockingConnection(self.amqp_params)

    def receive_msg(self, queue_name):
        channel = self.amqp_conn.channel()
        for method_frame, properties, body in  channel.consume(queue_name):
            print body
            channel.basic_ack(method_frame.delivery_tag)

        requeued_messages = channel.cancel()
        print 'Requeued %i messages' % requeued_messages
        channel.close()


    def fire_event(self, cid, event):
        test = CidEvent(cid, event)
        mq_property = pika.BasicProperties(headers={'messageType': 'com.haima.cloudplayer.servicecore.domain.cloudservice.StateEventCarrier'})
        mq_property.correlation_id = "12312312"
        channel = self.amqp_conn.channel()
        channel.basic_publish(exchange='exchange.cloudservice.channel.statemachine',
                              routing_key="com.haima.cloudplayer.servicecore.domain.cloudservice.StateEventCarrier",
                              body=str(test),
                              properties=mq_property)
        channel.close()


    def send_msg_access(self, msg):
        channel = self.amqp_conn.channel()
        channel.basic_publish(exchange='ACCESS-FANOUT-QUEUE-EXCHANGE', body=msg)
        channel.close()
        
    def send_wait_message(self, cid, index, show_time = True):
        avg_time = 60000
        msg = CloudMessage(cid)
        data = {}
        data['index'] = index
        data['time'] = str(avg_time*index)
        if show_time:
            avg_time = 99
            data['time'] = str(avg_time * index)
            data['timeStr'] = "%sm%ss" %(avg_time*index//60, avg_time*index%60)

        msg.data = data
        msg.operation = 1
        self.send_msg_access(msg)


    def send_choose_message(self, cid, index):
        msg = CloudMessage(cid)
        data = {}
        data['index'] = index
        msg.data = data
        msg.operation = 6
        self.send_msg_access(msg)

    def send_kicked_message(self, cid):
        msg = CloudMessage(cid)
        msg.operation = 2
        self.send_msg_access(msg)

    def send_error_message(self, cid):
        msg = CloudMessage(cid)
        msg.operation = 3
        self.send_msg_access(msg)

    def send_overtime_message(self,cid):
        msg = CloudMessage(cid)
        msg.operation = 4
        self.send_msg_access(msg)

    def send_ready_message(self,cid):
        msg = CloudMessage(cid)
        msg.operation = 10
        self.send_msg_access(msg)

    def send_refuse_message(self,cid):
        msg = CloudMessage(cid)
        msg.operation = 7
        self.send_msg_access(msg)

    def send_stoken_message(self,cid):
        msg = CloudMessage(cid)
        msg.operation = 11
        self.send_msg_access(msg)

    def send_resolution_message(self,cid):
        msg = CloudMessage(cid)
        msg.operation = 12
        self.send_msg_access(msg)

    def send_resume_message(self, cid):
        msg = CloudMessage(cid)
        msg.operation = 13
        self.send_msg_access(msg)

    def send_ready_stop_message(self, cid):
        msg = CloudMessage(cid)
        data = {}
        data['ready'] = str(1000)
        data['timeStr'] = "sdasda"
        msg.data = data
        msg.operation = 14
        self.send_msg_access(msg)

    def send_stop_message(self, cid):
        msg = CloudMessage(cid)
        msg.operation = 15
        self.send_msg_access(msg)

    def send_stopped_message(self, cid):
        msg = CloudMessage(cid)
        msg.operation = 16
        data = {}
        data['endTimeText'] = "3 minutes"
        msg.data = data
        self.send_msg_access(msg)

    def send_cancel_stop_message(self, cid):
        msg = CloudMessage(cid)
        msg.operation = 17
        self.send_msg_access(msg)

    def send_address_mesaage(self,cid):
        msg = CloudMessage(cid)
        msg.operation = 5
        data = {"audioUrl":"rtmp://172.16.10.238:1935/publishlive/mystreamaudio?st=5350786d557539524e776754346b79614b7035693369626249335a5959516775","countdownTime":60000,"inputUrl": "ws://172.16.10.238:7681/5350786d557539524e776754346b79614b7035693369626249335a5959516775","playingTime":5732502,"remindTime":300000,"resolution":"2","sToken":"5350786d557539524e776754346b79614b7035693369626249335a5959516775","videoUrl":"rtmp://172.16.10.238:1935/publishlive/mystream?st=5350786d557539524e776754346b79614b7035693369626249335a5959516775"}
        msg.data = data
        self.send_msg_access(msg)

    __mcExchanges = {
        "about_msg": "exchange.msgcenter.pushmsg",
        "client": "exchange.msgcenter.clientstate"
    }

    __mcRoutingKeys = {
        "singMsg": "com.haima.cloudplayer.msgcenter.domain.message.MsgCarrier",
        "groupMsg": "com.haima.cloudplayer.msgcenter.domain.message.GroupMsgCarrier",
        "kick": "com.haima.cloudplayer.msgcenter.domain.client.ClientKickCarrier",
        "alloc": "com.haima.cloudplayer.msgcenter.domain.message.AllocGroupCarrier"
    }

    def push_single_msg(self, cid, msg):
        mq_property = pika.BasicProperties(
            headers={'messageType': self.__mcRoutingKeys["singMsg"]})
        mq_property.correlation_id = "single_msg_" + str(random.uniform(10000, 1000000))
        body = SingleMsg(cid, msg)
        channel = self.amqp_conn.channel()
        channel.basic_publish(exchange=self.__mcExchanges["about_msg"], routing_key=self.__mcRoutingKeys["singMsg"], body=str(body), properties=mq_property)
        channel.close()

    def push_group_msg(self, group_list, msg):
        mq_property = pika.BasicProperties(
            headers={'messageType': self.__mcRoutingKeys["groupMsg"]})
        mq_property.correlation_id = "group_msg_" + str(random.uniform(10000, 1000000))
        body = GroupMsg(group_list, msg)
        channel = self.amqp_conn.channel()
        channel.basic_publish(exchange=self.__mcExchanges["about_msg"], routing_key=self.__mcRoutingKeys["groupMsg"], body=str(body), properties=mq_property)
        channel.close()

    def kick_client(self, cid):
        mq_property = pika.BasicProperties(
            headers={'messageType': self.__mcRoutingKeys["kick"]})
        mq_property.correlation_id = "kick_client_" + str(random.uniform(10000, 1000000))
        body = KickClient(cid)
        channel = self.amqp_conn.channel()
        channel.basic_publish(exchange=self.__mcExchanges["client"], routing_key=self.__mcRoutingKeys["kick"], body=str(body), properties=mq_property)
        channel.close()

    def alloc_group(self, cid, group_list):
        mq_property = pika.BasicProperties(
            headers={'messageType': self.__mcRoutingKeys["alloc"]})
        mq_property.correlation_id = "alloc_group_" + str(random.uniform(10000, 1000000))
        body = AllocGroup(cid, group_list)
        channel = self.amqp_conn.channel()
        channel.basic_publish(exchange=self.__mcExchanges["client"], routing_key=self.__mcRoutingKeys["alloc"], body=str(body), properties=mq_property)
        channel.close()


class CidEvent(object):
    __slots__ = ('cid', 'event')

    def __init__(self, cid, event):
        self.cid = cid
        self.event = event

    def __str__(self):
        class_path = "com.haima.cloudplayer.servicecore.domain.cloudservice."
        event_class_name = class_path + "StateEvent" + self.event
        class_name = class_path + "StateEventCarrier"
        return '{"@type":"%s","cid":%s,"event":{"@type":"%s","eventType":"%s"}}'\
               %(class_name, self.cid, event_class_name, self.event)

if __name__ == "__main__":
    cloud_mq = CloudAMQP()

    cloud_mq.fire_event("24", "AccessLinkSuccess")
