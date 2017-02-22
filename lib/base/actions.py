#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
from baseinfo import BaseInfo

class CommAction(BaseInfo):
    def __init__(self):
        super(CommAction, self).__init__()
        self.__attrs__ = ['client', 'device', 'action', 'data']


if __name__ == "__main__":
    test = CommAction()
    test2 = BaseInfo()
    test2.aaa = "12312"
    test.client = test2
    print test
    print json.dumps(test2)

    print json.dumps(test)
    aa = {}
    aa['client'] = {"aaa": "12312"}
    print aa
    print json.dumps(aa)
    xx = str(test)

    print xx
    print type(xx)

    print json.dumps(xx)