#!/usr/bin/env python
# -*- coding: UTF-8 -*-


class SingleMsg(object):
    __slots__ = ('cid', 'body')

    def __init__(self, cid, body):
        self.cid = cid
        self.body = body

    def __str__(self):
        class_name = "com.haima.cloudplayer.msgcenter.domain.message.MsgCarrier"
        return '{"@type":"%s", "cid":"%s", "body":"%s"}' % (class_name, self.cid, self.body)


class GroupMsg(object):
    __slots__ = ('group', 'body')

    def __init__(self, group, body):
        self.group = group
        self.body = body

    def __str__(self):
        class_name = "com.haima.cloudplayer.msgcenter.domain.message.GroupMsgCarrier"
        return '{"@type":"%s", "groupList":%s, "body":"%s"}' % (class_name, self.group, self.body)


if __name__ == '__main__':
    gmsg = GroupMsg(["g1", "g2", "g3"], "gmsg")
    print str(gmsg)
