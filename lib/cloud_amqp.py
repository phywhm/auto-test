#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import pika
import configuration as CONFIG
from base.cloud_message import CloudMessage

class CloudAMQP(object):
    def __init__(self, host=None, port=5672, virtual_host="/", password="Hm_Rabbit"):
        if host:
            credential = pika.PlainCredentials("hm_rabbit", password)
            self.amqp_params = pika.ConnectionParameters(host=host, port=port, virtual_host=virtual_host,
                                                         credentials=credential)
        else:
            credential = pika.PlainCredentials(CONFIG.AMQP_USER, CONFIG.AMQP_PASSWD)
            self.amqp_params = pika.ConnectionParameters(host=CONFIG.SAAS_HOST, port=CONFIG.AMQP_PORT, virtual_host=CONFIG.VIRTUAL_HOST,
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



if __name__ == "__main__":
    cloud_mq =  CloudAMQP(host="172.16.2.77")
    cloud_mq.send_ready_stop_message('78470')
