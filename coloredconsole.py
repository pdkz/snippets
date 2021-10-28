import os
import sys
import ctypes

class ConsoleColor(object):
    CLEAR   = 'clear'
    WHITE   = 'white'
    BLACK   = 'black'
    BLUE    = 'blue'
    GREEN   = 'green'
    RED     = 'red'
    YELLOW  = 'yellow'
    MAGENTA = 'magenta'
    CYAN    = 'cyan'

class ColoredConsole(object):
    colors = None
    def __init__(self, color):
        ColoredConsole.colors = color

    @classmethod
    def print(cls, *objects, **kwargs):
        pass

class ColoredConsoleWin32(ColoredConsole):
    if os.name == 'nt':
        STD_OUTPUT_HANDLE = -11

        # Foreground color definition
        FG_BLACK = 0x00
        FG_BLUE  = 0x01
        FG_GREEN = 0x02
        FG_RED   = 0x04

        FG_WHITE   = FG_BLUE | FG_GREEN | FG_RED
        FG_CYAN    = FG_BLUE | FG_GREEN
        FG_MAGENTA = FG_BLUE | FG_RED
        FG_YELLOW  = FG_GREEN | FG_RED

        FG_INTENSITY = 0x08

        # Background color definition
        BG_BLACK = 0x00
        BG_BLUE  = 0x10
        BG_GREEN = 0x20
        BG_RED   = 0x40

        BG_WHITE   = BG_BLUE | BG_GREEN | BG_RED
        BG_CYAN    = BG_BLUE | BG_GREEN
        BG_MAGENTA = BG_BLUE | BG_RED
        BG_YELLOW  = BG_GREEN | BG_RED

        BG_INTENSITY = 0x80

        fg_colors = {
            ConsoleColor.CLEAR   : FG_WHITE,
            ConsoleColor.BLACK   : FG_BLACK,
            ConsoleColor.BLUE    : FG_BLUE | FG_INTENSITY,
            ConsoleColor.GREEN   : FG_GREEN | FG_INTENSITY,
            ConsoleColor.RED     : FG_RED | FG_INTENSITY,
            ConsoleColor.WHITE   : FG_WHITE | FG_INTENSITY,
            ConsoleColor.CYAN    : FG_CYAN | FG_INTENSITY,
            ConsoleColor.MAGENTA : FG_MAGENTA | FG_INTENSITY,
            ConsoleColor.YELLOW  : FG_YELLOW | FG_INTENSITY,
        }

        bg_colors = {
            ConsoleColor.BLACK   : BG_BLACK,
            ConsoleColor.BLUE    : BG_BLUE | BG_INTENSITY,
            ConsoleColor.GREEN   : BG_GREEN | BG_INTENSITY,
            ConsoleColor.RED     : BG_RED | BG_INTENSITY,
            ConsoleColor.WHITE   : BG_WHITE | BG_INTENSITY,
            ConsoleColor.CYAN    : BG_CYAN | BG_INTENSITY,
            ConsoleColor.MAGENTA : BG_MAGENTA | BG_INTENSITY,
            ConsoleColor.YELLOW  : BG_YELLOW | BG_INTENSITY,
        }

        std_out_handler = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    def __init__(self):
        ColoredConsole.__init__(self, ColoredConsoleWin32.colors)

    @classmethod
    def print(cls, *objects, **kwargs):
        col = kwargs.get('col', 'clear')
        cls.set_color(col)
        sep = kwargs.get('sep', ' ')
        out = kwargs.get('file', sys.stdout)
        out.write(sep.join(objects) + '\n')
        cls.set_color(ConsoleColor.CLEAR)

    @classmethod
    def set_color(cls, fg_colorname=ConsoleColor.CLEAR, bg_colorname=ConsoleColor.BLACK):
        fg_color = cls.fg_colors.get(fg_colorname, ConsoleColor.CLEAR)
        bg_color = cls.bg_colors.get(bg_colorname, ConsoleColor.BLACK)

        ctypes.windll.kernel32.SetConsoleTextAttribute(cls.std_out_handler, fg_color | bg_color)

class ColoredConsoleLinux(ColoredConsole):
    # ANSI Color
    colors = {
        ConsoleColor.CLEAR  : '\033[0m',
        ConsoleColor.BLACK  : '\033[30m',
        ConsoleColor.RED    : '\033[31m',
        ConsoleColor.GREEN  : '\033[32m',
        ConsoleColor.YELLOW : '\033[33m',
        ConsoleColor.BLUE   : '\033[34m',
        ConsoleColor.MAGENTA: '\033[35m',
        ConsoleColor.CYAN   : '\033[36m',
        ConsoleColor.WHITE  : '\033[37m'
    }

    def __init__(self):
        ColoredConsole.__init__(self, ColoredConsoleLinux.colors)

    @classmethod
    def print(cls, *objects, **kwargs):
        col = kwargs.get('col', 'clear')
        sep = kwargs.get('sep', ' ')
        out = kwargs.get('file', sys.stdout)
        out.write(cls.colors.get(col, ConsoleColor.CLEAR) + sep.join(objects) + '\n')
        out.write(cls.colors.get(ConsoleColor.CLEAR))

def format_string(string, width, align):
    if width <= 0 :
        return string
    fmt = '{:^%d}' % width
    string = fmt.format(string)
    return string

class ColoredConsoleFactory(object):
    def __init__(self):
        pass

    @staticmethod
    def create():
        if os.name == 'nt':
            return ColoredConsoleWin32
        else :
            return ColoredConsoleLinux
