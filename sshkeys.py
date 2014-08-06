#!/usr/bin/env python
import argh
import ConfigParser
import json
import socket

from os.path import expanduser
from subprocess import check_call, CalledProcessError


def run_cmd(command):
    """ Runs a command and returns an array of its results

    :param command: String of a command to run within a shell
    :returns: Dictionary with keys relating to the execution's success
    """
    try:
        ret = check_call(command, shell=True)
        return {'success': True, 'return': ret, 'exception': None}
    except CalledProcessError, cpe:
        return {'success': False,
                'return': None,
                'exception': cpe,
                'command': command}


def get_hosts(inventory):
    """ Returns valid IP addresses from an INI file

    :param inventory: Path to an INI file
    :returns: List of strings
    """

    def valid_ip(address):
        try:
            # converts a string to 32-bit binary to test validity of address
            socket.inet_aton(address)
            return True
        except socket.error:
            return False

    # 'allow_no_value' will allow our INI file to not require a key-value pair
    config = ConfigParser.ConfigParser(allow_no_value=True)
    config.read(expanduser(inventory))

    # filter out invalid IP addresses in each section
    return set(option for section in config.sections()
               for option in config.options(section) if valid_ip(option))


def main(inventory=None, configuration=None):
    """ Given an inventory and configuration file, place SSH keys onto
        designated hosts

    :param inventory: Path to an INI file
    :param configuration: Path to a configuration file with credentials
    """

    with open(configuration, 'r') as fp:
        credentials = json.load(fp)
        username = credentials['username']
        password = credentials['password']

    hosts = get_hosts(inventory)
    for host in hosts:
        command = ('sshpass -p {password} ssh-copy-id'
                   ' -o UserKnownHostsFile=/dev/null'
                   ' -o StrictHostKeyChecking=no {username}@{host}')
        run_cmd(command.format(username=username, password=password, host=host))

argh.dispatch_command(main)
