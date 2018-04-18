#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import xtestlogger
from librtmp import RTMP
import time

logger = xtestlogger.get_logger(__name__)

class RTMPClient():
    def __init__(self, audio_url, video_url, stoken):
        self.audio_url = audio_url
        self.video_url = video_url
        self.stoken = stoken
        self.audio_client = RTMP(self.audio_url, live=True, token=self.stoken)
        self.video_client = RTMP(self.video_url, live=True, token=self.stoken)

        self.audio_client.connect()
        self.video_client.connect()

        self.audio_stream = self.audio_client.create_stream()
        self.video_stream = self.video_client.create_stream()

        self.recieve_done = False
        self.continue_recieve = True



    def recieve(self, size=1024):
        while self.continue_recieve:
            self.recieve_done = False
            audio_data = self.audio_stream.read(size)
            video_data = self.video_stream.read(size)
            self.recieve_done = True
            logger.info(len(video_data))
            if len(video_data) == 0:
                self.close()
            del audio_data
            del video_data


    def close(self):
        self.continue_recieve = False
        while True:
            if self.recieve_done:
                self.audio_stream.close()
                self.video_stream.close()
                self.audio_client.close()
                self.video_client.close()
                break
            time.sleep(0.5)




if __name__ == "__main__":
    client = RTMPClient("rtmp://172.16.10.244:1935/publishlive/mystreamaudio?st=426267667a70526e454a324a4445314469386f67334533624f337059712b4662",
                        "rtmp://172.16.10.244:1935/publishlive/mystream?st=426267667a70526e454a324a4445314469386f67334533624f337059712b4662",
                        '426267667a70526e454a324a4445314469386f67334533624f337059712b4662',
                        None)
    client.revieve(40960)
    client.close()