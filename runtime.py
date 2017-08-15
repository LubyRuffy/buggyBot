#!/usr/bin/python3.4

import curses
import buggy

print('\nWaking robot...\n')
bot = buggy.buggyBot()
print('Initialising Systems\n')
bot.update() ## Initialise all systems

actions = {
    curses.KEY_UP: bot.forwards,
    curses.KEY_DOWN: bot.backwards,
    curses.KEY_LEFT: bot.turn_left,
    curses.KEY_RIGHT: bot.turn_right
    }

def main(window):

    next_key = None
    while True:
        curses.halfdelay(1)
        if next_key is None:
            key = window.getch()
        else:
            key = next_key
            next_key = None
        if key != -1:
            # KEY DOWN
            curses.halfdelay(3)
            action = actions.get(key)
            if action is not None:
                action()
                bot.update()
            next_key = key
            while next_key == key:
                next_key = window.getch()
            # KEY UP
            bot.stop

if __name__ == '__main__':

    print("\nLet's do this!!\n")
    curses.wrapper(main)
