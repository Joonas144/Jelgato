from __future__ import absolute_import

import sys
import os
import re


if os.name == 'nt':  # sys.platform == 'win32':
    from serial.tools.list_ports_windows import comports
elif os.name == 'posix':
    from serial.tools.list_ports_posix import comports
else:
    raise ImportError("Sorry: no implementation for your platform ('{}') available".format(os.name))


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def grep(regexp, include_links=False):
    """\
    Search for ports using a regular expression. Port name, description and
    hardware ID are searched. The function returns an iterable that returns the
    same tuples as comport() would do.
    """
    r = re.compile(regexp, re.I)
    for info in comports(include_links):
        port, desc, hwid = info
        if r.search(port) or r.search(desc) or r.search(hwid):
            yield info


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def main():
    import argparse

    parser = argparse.ArgumentParser(description='Serial port enumeration')

    parser.add_argument(
        'regexp',
        nargs='?',
        help='only show ports that match this regex')

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='show more messages')

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='suppress all messages')

    parser.add_argument(
        '-n',
        type=int,
        help='only output the N-th entry')

    parser.add_argument(
        '-s', '--include-links',
        action='store_true',
        help='include entries that are symlinks to real devices')

    args = parser.parse_args()

    hits = 0
    # get iteraror w/ or w/o filter
    if args.regexp:
        if not args.quiet:
            sys.stderr.write("Filtered list with regexp: {!r}\n".format(args.regexp))
        iterator = sorted(grep(args.regexp, include_links=args.include_links))
    else:
        iterator = sorted(comports(include_links=args.include_links))

    return iterator

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def findArduino():
    noPortsFound = True
    while noPortsFound:
        ports = main()
        noPortsFound = ports.__len__() == 0

    for i, (port, full_name, info) in enumerate(ports, 0):
        print(full_name)
        if info == "USB VID:PID=2341:8037 SER=HIDPC":
            return port
