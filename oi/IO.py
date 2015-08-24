__author__ = 'aurcioli'


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
    @staticmethod
    def get(query):
        return input("[{}??{}] {}".format(colors.fg.lightgreen, colors.reset, query))

    @staticmethod
    def put(text, mode="info"):
        if mode == "info":
            print("[{}>>{}] {}".format(colors.fg.lightblue, colors.reset, text))

        elif mode == "warning":
            print("[{}!!{}] {}".format(colors.fg.yellow, colors.reset, text))

        elif mode == "critical" or mode == "error":
            print("[{}!!{}] {}{}".format(colors.fg.red, colors.reset, colors.fg.lightred, text))

        elif mode == "highlight":
            print("[{}>>{}] {}{}".format(colors.fg.lightblue, colors.reset, colors.fg.lightcyan, text))

        print(colors.reset, end = "", flush = True)
