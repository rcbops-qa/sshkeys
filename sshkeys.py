#!/usr/bin/env python
import argh
import ConfigParser
import os
import json
import socket

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


def get_targets(ini_file):

    def valid_ip(address):
        try:
            socket.inet_aton(address)
            return True
        except socket.error:
            return False

    config = ConfigParser.ConfigParser(allow_no_value=True)
    config.readfp(open(ini_file))
    _tmp = []
    for section in config.sections():
        options = config.options(section)
        for option in options:
            if valid_ip(option):
                _tmp.append(option)
    return set(_tmp)


def main(inventory=None, credentials=None):
    targets = get_targets(os.path.expanduser(inventory))
    for target in targets:
        with open(credentials, 'r') as fp:
            ini_file = json.load(fp)
            username = ini_file['username']
            password = ini_file['password']
            command = ('sshpass -p {} ssh-copy-id'
                       ' -o UserKnownHostsFile=/dev/null'
                       ' -o StrictHostKeyChecking=no {}@{}')
            run_cmd(command.format(password, username, target))


argh.dispatch_command(main)
