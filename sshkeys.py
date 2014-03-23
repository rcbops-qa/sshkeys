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

def valid_host(hosts, name):
    for host in hosts:
        if host in name:
            return True
    return False

def sshkey(default_pass="password", hosts=None):
    api = autoconfigure()
    sshpass = ("ping -c 1 -W 5 {host} && sshpass -p {password} ssh-copy-id root@{host}")
    hosts = hosts.split(",")
    nodes = (Node(node, api=api) for node in Node.list(api=api) if valid_host(hosts, node))
    for node in nodes:
        host = node['ipaddress']
        password = node.get('password', default_pass)
        command = sshpass.format(host=host, password=password)
        run_cmd(command)

argh.dispatch_command(sshkey)
