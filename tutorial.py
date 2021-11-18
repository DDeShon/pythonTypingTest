import curses
from curses import wrapper
import time

# set up console screen for the typing test
def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(1, 0, "Welcome to the Typing Speed Test!")
    stdscr.addstr("\n\nPress any key to begin!")
    stdscr.refresh()
    stdscr.getkey()

# function to place typed text over top of default text
def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"\nWPM: {wpm}")

    # test the characters typed to verify if they match default text
    for i, char in enumerate(current):
        correct_char = target[i]
        # if the input is correct color it green
        color = curses.color_pair(1)
        # if input is incorrect color it red
        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)

# set up default text for typing test
def wpm_test(stdscr):
    target_text = "Hello world this is some test text for the app!"
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        # break out of app if 'escape' key is pressed
        if ord(key) == 27:
            break
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

# set up the main function
def main(stdscr):
    # set up color scheme for typing test
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(3, 0, "You completed the test! Press any key to continue..")
        key = stdscr.getkey()

        # break out of app if 'escape' key is pressed
        if ord(key) == 27:
            break


wrapper(main)
