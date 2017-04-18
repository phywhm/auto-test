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
from lib import clouddata

que = []
MAX_INSTANCE_NUM = 100000
CALL_BACK_TIME = formatdata.random_int(1000, 1500)
DEFAULT_ROUTE = "99,99"

CUSTOM_MAX_INSTACNE = None
CUSTOM_CALLBACK_TIME = None
CUSTOM_ROUTE = None
MAX_ERROR_TIMES = 0


class MockHandler(BaseHTTPRequestHandler):
    error_times = 0
    route_map = {}
    routes = ['2,4', '3,4', '5,4']
    def do_POST(self):
        global CUSTOM_MAX_INSTACNE
        global CUSTOM_CALLBACK_TIME
        global CUSTOM_ROUTE
        global MAX_ERROR_TIMES
        max_instance = MAX_INSTANCE_NUM if CUSTOM_MAX_INSTACNE is None else CUSTOM_MAX_INSTACNE
        self.response = {"operation": "com.haima.cloudplayer.controller.instance.apply", "code": 1000, "message": "ok",
                         "memo": "operation successfully"}
        datas = self.rfile.read(int(self.headers['content-length']))
        print datas
        datas = urllib.unquote(datas).decode("utf-8", 'ignore')  # 指定编码方式
        datas = json.loads(datas)

        if datas['operation'] == "com.haima.cloudplayer.controller.instance.apply":
            serviceId = int(datas['param']['cidInfo']['info'].split(',')[0])
            if datas['param']['flagIfIds'] != "0":
                serviceId =  datas['param']['flagIfIds'].split(',')[0] + "-" + datas['param']['cidInfo']['info'].split(',')[0]

            pkg_name = datas['param']['packageName']
            if pkg_name.lower().startswith("noapp"):
                self.response['response'] = {'code': 0, 'success': False, 'serviceId': None, 'state': 'NoAppInfoFound'}
            elif pkg_name.lower().startswith("noidle"):
                self.response['response'] = {'code': 0, 'success': False, 'serviceId': 0, 'state': 'NoIdleInstance'}
            else:
                if len(que) >= int(max_instance):
                    self.response['response'] = {'code': 0, 'success': False, 'serviceId': 0, 'state': 'NoIdleInstance'}
                else:
                    que.append(serviceId)
                    self.response['response'] = {'code': 0, 'success': True, 'serviceId': serviceId, 'state': 'Preparing'}
                    t = threading.Thread(target=self.notify_instance, args=(serviceId, "01",))
                    t.start()
        elif datas['operation'] == "com.haima.cloudplayer.controller.instance.release":
            self.response['operation'] = "com.haima.cloudplayer.controller.instance.release"

            if datas['param'] in que:
                try:
                    que.remove(int(datas['param']))
                except:
                    que.remove(datas['param'])

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
        elif datas['operation'] == "com.haima.cloudplayer.controller.router.getInterface":
            router = DEFAULT_ROUTE if CUSTOM_ROUTE is None else CUSTOM_ROUTE
            self.response['operation'] = 'com.haima.cloudplayer.controller.router.getInterface'
            self.response['response'] = {"flagIfIds": router}
        elif datas['operation'] == "test.change.params":
            if 'max_num' in datas:
                CUSTOM_MAX_INSTACNE = int(datas['max_num'])
            if 'callback_interval' in datas:
                CUSTOM_CALLBACK_TIME = int(datas['callback_interval'])
            if 'max_error_times' in datas:
                MAX_ERROR_TIMES = int(datas['max_error_times'])
                MockHandler.error_times = 0
            if 'custom_route' in datas:
                CUSTOM_ROUTE = datas['custom_route']
        elif datas['operation'] == "test.unset.params":
            if datas['param'] == "max_num" or datas['param'] == "all":
                CUSTOM_MAX_INSTACNE = None
            if datas['param'] == "callback_interval" or datas['param'] == "all":
                CUSTOM_CALLBACK_TIME = None
            if datas['param'] == "custom_route" or datas['param'] == "all":
                CUSTOM_ROUTE = None
            if datas['param'] == "max_error_times" or datas['param'] == "all":
                MAX_ERROR_TIMES = 0
                MockHandler.error_times = 0

        print "----", MockHandler.error_times
        if MAX_ERROR_TIMES != 0 and MockHandler.error_times <= MAX_ERROR_TIMES:
            if MockHandler.error_times != 0:
                MockHandler.error_times += 1
                return
            MockHandler.error_times += 1

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
        intervel = CUSTOM_CALLBACK_TIME if CUSTOM_CALLBACK_TIME is not None else CALL_BACK_TIME
        if int(intervel) == 0:
            return
        time.sleep(int(intervel)/1000)
        params = clouddata.generate_comm_request(203)
        params.data = clouddata.generate_instance_info(cid, status)
        print "=======", params, self.client_address
        common.run_request("http://" + self.client_address[0] + ":8010/rest/api", method="POST", commparams=params)


if __name__ == "__main__":
    server_address = ('', 8080)
    server = HTTPServer(server_address, MockHandler)
    server.serve_forever()
