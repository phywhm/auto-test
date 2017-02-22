#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import commands

def run_command(cmd):
    return commands.getstatusoutput(cmd)

def run_remote_command(cmd, server, port=22, user='root', indetify_key=None):
    ssh_option = "-o StrictHostKeyChecking=no -o connectTimeout=20 -p %s" %(port)
    if indetify_key is not None:
        ssh_option += "-i %s" %s(indetify_key)
    cmd = "ssh %s %s@%s '%s'" %(ssh_option, user, server, cmd)
    return run_command(cmd)

def run_local_comand(cmd):
    return run_command(cmd)


print run_remote_command("ls", "172.16.2.77")