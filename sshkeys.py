#!/usr/bin/env python

import argh
from chef import Node, autoconfigure
from subprocess import check_call, CalledProcessError


def run_cmd(command):
    """
    @param cmd
    @return A map based on pass / fail run info
    """
    try:
        ret = check_call(command, shell=True)
        return {'success': True, 'return': ret, 'exception': None}
    except CalledProcessError, cpe:
        return {'success': False,
                'return': None,
                'exception': cpe,
                'command': command}


def sshkey(default_pass="password"):
    sshpass = ("sshpass -p {1} ssh -o UserKnownHostsFile=/dev/null "
               "-o StrictHostKeyChecking=no -o LogLevel=quiet "
               "-o ServerAliveInterval=5 -o ServerAliveCountMax=1 -l root {0}")
    api = autoconfigure()
    nodes = (Node(node, api=api) for node in Node.list(api=api))
    for node in nodes:
        host = node['ipaddress']
        command = "ssh-copy-id root@{0}".format(host)
        password = node.get('password', default_pass)
        run_cmd(sshpass.format(command, password))

argh.dispatch_command(sshkey)
