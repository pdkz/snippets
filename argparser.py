#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import argparse

VERSION    = (1, 0, 1)
MIN_PYTHON_VERSION  = (2, 7)

class _Options:
    help = False
    version = False
    confpath = ''

def check_python_version(min_python_version):
    ver = sys.version_info

    if ver[0] == 3:
        print('Python 3 is not supported.\n',
              'Please use Python 2.7.x instead.',
              file=sys.stderr)
        sys.exit()

    major_ver, minor_ver = min_python_version

    if ver[0] == 2:
        if ver[1] < min_python_version[1]:
            print('Python version %s unsupported.\n'
                  'Please use Python 2.7.x instead.'
                   % sys.version.split(' ')[0], file=sys.stderr)
            sys.exit()

def check_administrator():
    is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    if is_admin != True :
        print('You are NOT an Administrator.\n'
             'Need to run this script as an Administrator.',
             file=sys.stderr)
        sys.exit()

def get_prog(file):
    prog, ext = os.path.splitext(os.path.basename(file))
    return prog

def _print_version():
    major = VERSION[0]
    minor = VERSION[1]
    build = VERSION[2]

    _printf('%s %d.%d.%d', get_prog(__file__), major, minor, build)

def _print_usage():
    parser = argparse.ArgumentParser(prog=get_prog(__file__),
                                     usage="%(prog)s <command>",
                                     description='program description')

    parser._positionals.title = 'Commands'
    parser._optionals.title   = 'General Options'

    for item in commands.items():
        name, cmd = item
        parser.add_argument(name, help=cmd.summary)

    parser.add_argument('-c',
                        '--conf',
                        action='store',
                        type=str,
                        help='Specify a file path of config file.'
                        )
    parser.add_argument('-p',
                        '--proxy',
                        action='store',
                        type=str,
                        help='Specify a proxy server in the form\n[user:passwd@]proxy.server:port'
                        )
    parser.add_argument('-v',
                        '--version',
                        help='Show version and exit.'
                        )

    parser.print_help()

def _parse_optarg(idx, args):
    try:
        opt = args[idx + 1]
        if opt.startswith('-'):
            _print_usage()
            return False, None
    except IndexError:
        _print_usage()
        return False, None
    return True, opt

def _parse_args(args):
    cmd = None
    opt = _Options()
    arg = []
    b = True

    for i in range(len(args)):
        a = args[i]
        if i == 0 and not a.startswith('-'):
            cmd = a
            arg = args[i + 1:]

        if a == '-h' or a == '--help':
            opt.help = True
        elif a == '-v' or a == '--version':
            opt.version = True
        elif a == '-c' or a == '--conf':
            b, opt.confpath = _parse_optarg(i, args)
        #elif not a.startswith('-'):
        #    cmd = a
        #    arg = args[i + 1:]
        if b == False:
            break

    return b, cmd, opt, arg

def main():
    b, cmd, opt, arg = _parse_args(orig_args)
    if b == False:
        _print_usage();
        sys.exit()

    if cmd == 'command':
        check_administrator()

    if cmd not in commands:
        # need to define commands
        if opt.help == True:
            _print_usage()
            sys.exit()
        elif opt.version == True:
            _print_version()
            sys.exit()
        _print_usage()
        sys.exit()

    prog = get_prog(__file__)

if __name__ == '__main__':
  main(sys.argv[1:])
  
