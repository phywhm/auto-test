#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import urllib
import json
import io
import shutil
from lib.untils import formatdata
from lib import common
import threading
import time
from lib import requests

que = []
MAX_INSTANCE_NUM = 100000
CALL_BACK_TIME = formatdata.random_int(1000, 1500)

CUSTROM_MAX_INSTACNE = None
CUSTROM_CALLBACK_TIME = None


class MockHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global CUSTROM_MAX_INSTACNE
        global CUSTROM_CALLBACK_TIME
        max_instance = MAX_INSTANCE_NUM if CUSTROM_MAX_INSTACNE is None else CUSTROM_MAX_INSTACNE
        self.response = {"operation": "com.haima.cloudplayer.controller.instance.apply", "code": 1000, "message": "ok",
                         "memo": "operation successfully"}
        datas = self.rfile.read(int(self.headers['content-length']))
        datas = urllib.unquote(datas).decode("utf-8", 'ignore')  # 指定编码方式
        datas = json.loads(datas)
        print datas
        if datas['operation'] == "com.haima.cloudplayer.controller.instance.apply":
            serviceId = int(datas['param']['cidInfo']['info'].split(',')[0])
            pkg_name = datas['param']['packageName']
            if pkg_name.lower().startswith("noapp"):
                self.response['response'] = {'code': 0, 'success': False, 'serviceId': None, 'state': 'NoAppInfoFound'}
            else:
                if len(que) >= int(max_instance):
                    self.response['response'] = {'code': 0, 'success': False, 'serviceId': 0, 'state': 'NoIdleInstance'}
                else:
                    que.append(serviceId)
                    self.response['response'] = {'code': 0, 'success': True, 'serviceId': serviceId, 'state': ''}
                    t = threading.Thread(target=self.notify_instance, args=(serviceId, "01",))
                    t.start()
        elif datas['operation'] == "com.haima.cloudplayer.controller.instance.release":
            self.response['operation'] = "com.haima.cloudplayer.controller.instance.release"
            if datas['param'] in que:
                que.remove(int(datas['param']))

        elif datas['operation'] == "com.haima.cloudplayer.controller.instance.refreshSToken":
            self.response['operation'] = "com.haima.cloudplayer.controller.instance.refreshSToken"
            self.response['response'] = True
            serviceId = datas['param']['serviceId']
            t = threading.Thread(target=self.notify_instance, args=(serviceId, "23"))
            t.start()
        elif datas['operation'] == "com.haima.cloudplayer.controller.instance.updateResolution":
            self.response['operation'] = "com.haima.cloudplayer.controller.instance.updateResolution"
            self.response['response'] = True
            serviceId = datas['param']['serviceId']
            t = threading.Thread(target=self.notify_instance, args=(serviceId, "31"))
            t.start()
        elif datas['operation'] == "test.change.params":
            if 'max_num' in datas:
                CUSTROM_MAX_INSTACNE = int(datas['max_num'])
            if 'callback_interval' in datas:
                CUSTROM_CALLBACK_TIME = int(datas['callback_interval'])
        elif datas['operation'] == "test.unset.params":
            CUSTROM_MAX_INSTACNE = None
            CUSTROM_CALLBACK_TIME = None

        self.send_myresponse(json.dumps(self.response))

    def send_myresponse(self, content):
        enc = "UTF-8"
        content = content.encode(enc)
        f = io.BytesIO()
        f.write(content)
        f.seek(0)
        self.send_response(200)
        # self.send_header("Content-type","text/html; charset=%s" % enc)
        self.send_header("Content-type", "application/json; charset=%s" % enc)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        shutil.copyfileobj(f, self.wfile)

    def notify_instance(self, cid, status):
        intervel = CUSTROM_CALLBACK_TIME if CUSTROM_CALLBACK_TIME is not None else CALL_BACK_TIME
        time.sleep(int(intervel)/1000)
        params = requests.generate_comm_request(203)
        params.data = requests.generate_instance_info(cid, status)
        print params
        common.run_request("http://" + self.client_address[0] + ":8081/s/rest/api", method="POST", commparams=params)


if __name__ == "__main__":
    server_address = ('', 8080)
    server = HTTPServer(server_address, MockHandler)
    server.serve_forever()
