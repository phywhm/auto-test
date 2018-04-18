#!/usr/bin/env python
# -*- coding: UTF-8 -*-


class CloudStatics(object):
    __slots__ = ('xtotal', 'success', 'fail', 'waiting', 'no_wait', 'd_instance', 'w_instance', 'no_instance', 'stop',
                 'overtime', 'kicked', 'error', 'others')

    def __init__(self):
        self.xtotal = 0
        self.success = 0
        self.fail = 0
        self.waiting = 0
        self.no_wait = 0
        self.d_instance = 0
        self.w_instance = 0
        self.no_instance = 0
        self.stop = 0
        self.overtime = 0
        self.kicked = 0
        self.error = 0
        self.others = 0

    def add_num(self, cloud_status):
        self.xtotal += 1
        if cloud_status.success:
            self.success += 1
        else:
            self.fail += 1

        if cloud_status.waiting:
            self.waiting += 1
            if cloud_status.instance:
                self.w_instance += 1
            else:
                self.no_instance += 1
        else:
            if cloud_status.instance:
                self.d_instance += 1
            else:
                self.no_instance += 1
            self.no_wait += 1

        if cloud_status.release == "kicked":
            self.kicked += 0
        elif cloud_status.release == "overtime":
            self.overtime += 1
        elif cloud_status.release == "stop":
            self.stop += 1
        elif cloud_status.release == "crash":
            self.error += 1
        else:
            self.others += 1

    def print_statics(self):
        print "Start play games: {self.xtotal}".format(self=self)
        print "cuccess: {self.success}; fail: {self.fail}".format(self=self)

        print ""
        print "cuccess: {self.success}".format(self=self)
        print "waiting: {self.waiting}; not waiting: {self.no_wait}".format(self=self)

        print ""
        print "cuccess: {self.success}".format(self=self)
        print "wait and get instance: {self.w_instance}; wait but no instance: {self.no_instance}; get instance directly: {self.d_instance}".format(
            self=self)

        print ""
        print "cuccess: {self.success}".format(self=self)
        print "stop: {self.stop}; overtime: {self.overtime}; kicked: {self.kicked}; error: {self.error}; others: {self.others}".format(self=self)



if __name__ == "__main__":
    import time
    from clouduser import CloudUser
    instances = []
    cloud_statics = CloudStatics()
    for i in range(20):
        clouduser01 = CloudUser('cpd12521277'+str(i), '029694a0fafac97c5435a1a97a909222', "9599e53c")
        inst = clouduser01.start_instance("com.netease.stzb.haima")
        instances.append(inst)

    time.sleep(10)
    for inst in instances:
        inst.stop_instance()
        cloud_statics.add_num(inst.cloud_status)

    cloud_statics.print_statics()