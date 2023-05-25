__author__ = 'xsank'

import re
import sys


_PLATFORM = sys.platform


def check_ip(ip):
    pattern = re.compile(
        '^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    return bool(pattern.match(ip))


def check_port(port):
    return 0 < int(port) < 65536 if port and port.isdigit() else False


class Platform(object):

    @staticmethod
    def detail():
        return _PLATFORM

    @staticmethod
    def is_win():
        return _PLATFORM.startswith('win')

    @staticmethod
    def is_linux():
        return _PLATFORM.startswith('linux')

    @staticmethod
    def is_mac():
        return _PLATFORM.startswith('darwin')
