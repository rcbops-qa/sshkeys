#!/usr/bin/env python
import argh
import ConfigParser
import os
import json

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
    config = ConfigParser.ConfigParser(allow_no_value=True)
    config.readfp(open(ini_file))
    return config.get('target')


def main(inventory=None, credentials=None):
    targets = get_targets(os.path.expanduser(inventory))
    for target in targets:
        with open(credentials, 'r') as stream:
            credentials = json.loads(stream)
            username = credentials['username']
            password = credentials['password']
            command = "sshpass -p {} ssh-copy-id {}@{}".format(password,
                                                               username,
                                                               target)
            run_cmd(command)


argh.dispatch_command(main)
