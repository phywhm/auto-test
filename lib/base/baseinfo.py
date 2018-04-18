#!/usr/bin/env python
# -*- coding: UTF-8 -*-


class BaseInfo(dict):
    def __init__(self, mapping={}):
        super(BaseInfo, self).__init__(mapping)
        self.__attrs__ = []


    def __setattr__(self, key, value):
        if key == "__attrs__":
            object.__setattr__(self, key, value)
        elif not self.__attrs__:
            dict.__setitem__(self, key, value)
        elif key in self.__attrs__:
            dict.__setitem__(self, key, value)
        else:
            raise AttributeError

    def __getattr__(self, item):
        if item in self.__attrs__:
            return dict.__getitem__(self, item)
        elif not self.__attrs__:
            return dict.__getitem__(self, item)
        else:
            raise AttributeError

    def __setitem__(self, key, value):
        pass




if __name__ == "__main__":
    test = BaseInfo()
    test.ssss = "sdfa"
    aa = {"aa": "123", "bb": {"cc": "123"}}
    bb = '{"aa": "123", "bb": {"cc": "123"}}'
    print dict(bb)
    test = BaseInfo(aa)
    print type(test.bb)
    print test.aa
    import json
    print(json.dumps(test))