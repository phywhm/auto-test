#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from baseinfo import BaseInfo


class ActionInfo(BaseInfo):
    def __init__(self):
        super(ActionInfo, self).__init__()
        self.__attrs__ = ['actId', 'protocol', 'transId', 'did', 'sign', 'random','sdkType']