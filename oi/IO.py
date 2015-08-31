__author__ = 'aurcioli'
import sys

class colors:
    '''Colors class:
        reset all colors with colors.reset
        two subclasses fg for foreground and bg for background.
        use as colors.subclass.colorname.
        i.e. colors.fg.red or colors.bg.green
        also, the generic bold, disable, underline, reverse, strikethrough,
        and invisible work with the main class
        i.e. colors.bold
    '''
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'


class IO:
    logo = ("\n"
        "                         _           _             _\n"
        "                        | |         (_)           | |\n"
        " ___  ___  __ _ _ __ ___| |__   __ _ _  __ _ _ __ | |_\n"
        "/ __|/ _ \/ _` | '__/ __| '_ \ / _` | |/ _` | '_ \| __|\n"
        "\__ \  __/ (_| | | | (__| | | | (_| | | (_| | | | | |_\n"
        "|___/\___|\__,_|_|  \___|_| |_|\__, |_|\__,_|_| |_|\__|\n"
        "                                __/ |\n"
        "                               |___/\n"
        "\n")

    my_blue = colors.fg.lightblue if sys.platform == "darwin" else colors.fg.blue
    my_green = colors.fg.lightgreen if sys.platform == "darwin" else colors.fg.green
    my_red = colors.fg.lightred if sys.platform == "darwin" else colors.fg.red
    fall_back_lb = colors.fg.lightblue if sys.platform == "darwin" else colors.fg.cyan

    @staticmethod
    def get(query):
        return input("[{}??{}] {}".format(IO.my_green, colors.reset, query))

    @staticmethod
    def print_logo():
        print("{}{}{}".format(colors.fg.orange, IO.logo, colors.reset))

    @staticmethod
    def put(text, mode="info"):
        try:
            if mode == "info":
                print("[{}>>{}] {}".format(IO.fall_back_lb, colors.reset, text))

            elif mode == "warning":
                print("[{}!!{}] {}".format(colors.fg.orange, colors.reset, text))

            elif mode == "critical" or mode == "error":
                print("[{}!!{}] {}{}".format(colors.fg.red, colors.reset, IO.my_red, text))

            elif mode == "highlight":
                print("[{}>>{}] {}{}".format(colors.fg.purple, colors.reset, IO.fall_back_lb, text))

            print(colors.reset, end = "", flush = True)
        except UnicodeEncodeError:
            print("[{}!!{}] {}{}".format(colors.fg.red, colors.reset, colors.fg.lightred, "Unicode character not supported - skipping print to console"))
