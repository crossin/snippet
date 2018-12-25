# coding:utf8
# 炫彩版
import os
import sys
import platform
import random
import time


class UI(object):
    def __init__(self):
        os_name = platform.uname()[0]
        self.IS_WIN = os_name == 'Windows'
        self.IS_MAC = os_name == 'Darwin'
        if self.IS_WIN:
            self.RED = 0x0C
            self.GREY = 0x07
            self.BLUE = 0x09
            self.CYAN = 0x0B
            self.LINK = 0x30
            self.BLACK = 0x0
            self.GREEN = 0x0A
            self.WHITE = 0x0F
            self.PURPLE = 0x0D
            self.YELLOW = 0x0E
        else:
            self.RED = '\033[1;31m'
            self.GREY = '\033[38m'
            self.BLUE = '\033[1;34m'
            self.CYAN = '\033[36m'
            self.LINK = '\033[0;36;4m'
            self.BLACK = '\033[0m'
            self.GREEN = '\033[32m'
            self.WHITE = '\033[37m'
            self.PURPLE = '\033[35m'
            self.YELLOW = '\033[33m'
        self.p = self.win_print if self.IS_WIN else self.os_print

    def clear(self):
        os.system('cls' if self.IS_WIN else 'clear')
        return self

    def win_reset(self, color):
        from ctypes import windll
        handler = windll.kernel32.GetStdHandle(-11)
        return windll.kernel32.SetConsoleTextAttribute(handler, color)

    def win_print(self, msg, color, enter=True):
        color = color or self.BLACK
        self.win_reset(color | color | color)
        sys.stdout.write(('%s\n' if enter else '%s') % msg)
        self.win_reset(self.RED | self.GREEN | self.BLUE)
        return self

    def os_print(self, msg, color, enter=True):
        color = color or self.BLACK
        sys.stdout.write(
            ('%s%s%s\n' if enter else '%s%s%s') % (color, msg, self.BLACK))
        return self


def tree(ui, level=3):
    a = list(range(0, (level + 1) * 4, 2))
    b = a[0:2]
    for i in range(2, len(a) - 2, 2):
        b.append(a[i])
        b.append(a[i + 1])
        b.append(a[i])
        b.append(a[i + 1])
    b.append(a[-2])
    b.append(a[-1])
    light = True
    while True:
        ui.clear()
        ui.p(u'\t圣诞节快乐!\n\t\t\tMedici.Yan 2015', ui.RED)
        print
        light = not light
        lamp(ui, b, light)
        for i in range(2, len(b)):
            ui.p(
                '%s/' % (' ' * b[len(b) - i - 1]), ui.GREEN, enter=False)
            neon(ui, 2 * b[i] + 1)
            ui.p('\\', ui.GREEN, enter=True)
        time.sleep(1.2)


def neon(ui, space_len):
    colors = [ui.RED, ui.GREY, ui.BLUE, ui.CYAN, ui.YELLOW]
    for i in range(space_len):
        if random.randint(0, 16) == 5:
            ui.p('o', colors[random.randint(0, len(colors) - 1)], enter=False)
        else:
            ui.p(' ', ui.RED, enter=False)


def lamp(ui, tree_arr, light):
    colors = [ui.WHITE, ui.BLUE]
    if not light:
        colors.reverse()
    ui.p(' ' * (tree_arr[-1] + 1), ui.BLACK, enter=False)
    ui.p('|', colors[1])
    ui.p(' ' * tree_arr[-1], ui.BLACK, enter=False)
    ui.p('\\', colors[1], enter=False)
    ui.p('|', colors[0], enter=False)
    ui.p('/', colors[1])
    ui.p(' ' * tree_arr[-2], ui.BLACK, enter=False)
    ui.p('-', colors[0], enter=False)
    ui.p('-', colors[1], enter=False)
    ui.p('=', colors[0], enter=False)
    ui.p('O', colors[1], enter=False)
    ui.p('=', colors[0], enter=False)
    ui.p('-', colors[1], enter=False)
    ui.p('-', colors[0], enter=True)

    ui.p(' ' * tree_arr[-1], ui.BLACK, enter=False)
    ui.p('/', colors[1], enter=False)
    ui.p('|', colors[0], enter=False)
    ui.p('\\', colors[1])
    ui.p(' ' * tree_arr[-2], ui.BLACK, enter=False)
    ui.p('/  ', ui.GREEN, enter=False)
    ui.p('|', colors[1], enter=False)
    ui.p('  \\', ui.GREEN, enter=True)


def main():
    ui = UI()
    max_rows = 4
    tree(ui, max_rows)

if __name__ == '__main__':
    main()
