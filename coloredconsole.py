import os
import sys
import json
import ctypes
import urllib2

class ColoredConsole(object):
    if os.name == 'nt' :
        """
           Color definition for Windows
        """

        STD_OUTPUT_HANDLE = -11

        """
            Foreground color definition
        """

        FG_BLACK = 0x00
        FG_BLUE  = 0x01
        FG_GREEN = 0x02
        FG_RED   = 0x04

        FG_WHITE   = FG_BLUE | FG_GREEN | FG_RED
        FG_CYAN    = FG_BLUE | FG_GREEN
        FG_MAGENTA = FG_BLUE | FG_RED
        FG_YELLOW  = FG_GREEN | FG_RED

        FG_INTENSITY = 0x08

        """
            Background color definition
        """

        BG_BLACK = 0x00
        BG_BLUE  = 0x10
        BG_GREEN = 0x20
        BG_RED   = 0x40

        BG_WHITE   = BG_BLUE | BG_GREEN | BG_RED
        BG_CYAN    = BG_BLUE | BG_GREEN
        BG_MAGENTA = BG_BLUE | BG_RED
        BG_YELLOW  = BG_GREEN | BG_RED

        BG_INTENSITY = 0x80

        fg_colors = { 'black'  : FG_BLACK,
                      'blue'   : FG_BLUE | FG_INTENSITY,
                      'green'  : FG_GREEN | FG_INTENSITY,
                      'red'    : FG_RED | FG_INTENSITY,
                      'white'  : FG_WHITE | FG_INTENSITY,
                      'cyan'   : FG_CYAN | FG_INTENSITY,
                      'magenta': FG_MAGENTA | FG_INTENSITY,
                      'yellow' : FG_YELLOW | FG_INTENSITY,
                     }

        bg_colors = { 'black'  : BG_BLACK,
                      'blue'   : BG_BLUE | BG_INTENSITY,
                      'green'  : BG_GREEN | BG_INTENSITY,
                      'red'    : BG_RED | BG_INTENSITY,
                      'white'  : BG_WHITE | BG_INTENSITY,
                      'cyan'   : BG_CYAN | BG_INTENSITY,
                      'magenta': BG_MAGENTA | BG_INTENSITY,
                      'yellow' : BG_YELLOW | BG_INTENSITY,
                     }
        std_out_handler = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    else :
        # ANSI Color
        colors = {
            'clear' : '\033[0m',
            'black' : '\033[30m',
            'red'   : '\033[31m',
            'green' : '\033[32m',
            'yellow': '\033[33m',
            'blue'  : '\033[34m',
            'purple': '\033[35m',
            'cyan'  : '\033[36m',
            'white' : '\033[37m'
        }

    @classmethod
    def blue(cls, string, width=0, align=None):
        string = format_string(string, width, align)
        return '%s%s' % (cls.colors['blue'], string)

    @classmethod
    def green(cls, string, width=0, align=None):
        string = format_string(string, width, align)
        return '%s%s' % (cls.colors['green'], string)

    @classmethod
    def white(cls, string, width=0, align=None):
        string = format_string(string, width, align)
        return '%s%s' % (cls.colors['white'], string)

    @classmethod
    def _write_console(string):
        sys.stdout.write('%s' % string)

    @classmethod
    def get_colored_string(cls, string, col='white', width=0, align=None):
        string = format_string(string, width, align)
        return '%s%s' % (cls.colors[col], string)

    @classmethod
    def set_color(cls, fg_colorname = 'white', bg_colorname = 'black'):
        """
           Windows only
        """
        fg_color = cls.fg_colors[fg_colorname]
        bg_color = cls.bg_colors[bg_colorname]

        ctypes.windll.kernel32.SetConsoleTextAttribute(cls.std_out_handler, fg_color | bg_color)

def format_string(string, width, align):
    if width <= 0 :
        return string
    fmt = '{:^%d}' % width
    string = fmt.format(string)
    return string
