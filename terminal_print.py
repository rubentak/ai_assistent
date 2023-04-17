# Print function to slowly print the text except when the user presses Enter
# With pressing enter, the full answer is printed instantly
from rich import print
from rich.console import Console
from pynput import keyboard
import time
import sys

console = Console()

def print_answer(answer):
    print_complete = False
    break_program = False

    def on_press(key):
        nonlocal break_program
        if key == keyboard.Key.enter:
            console.print('Printout activated', style='bold red')
            break_program = True
            return False

    listener_thread = keyboard.Listener(on_press=on_press)
    listener_thread.start()

    try:
        for line in answer.splitlines():
            for word in line.split():
                console.print(word, end=' ')
                sys.stdout.flush()
                time.sleep(0.30)
                if break_program:
                    break

            sys.stdout.write('\n')

            if line == answer.splitlines()[-1] and word == line.split()[-1]:
                console.print('\nPrintout completed', style='bold green')
                print_complete = True
                break_program = True
            if print_complete:
                break

    finally:
        listener_thread.join()

