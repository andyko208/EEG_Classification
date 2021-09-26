import pydirectinput

import random
import time
import winsound
import sys


def curr_cur():
    print('Current cursor x: {} y: {}'.format(pydirectinput.position()[0], pydirectinput.position()[1]))

def wandering(dur=5):

    moves = ('a', 'd', 'space')
    turns = (150, -150)
    t_init = time.time()
    dur = 10
    while (time.time() - t_init) < dur:
        pydirectinput.keyDown('w')
        move_var = random.choice(moves)
        x = int(pydirectinput.position()[0])
        y = int(pydirectinput.position()[1])
        turn_var = int(random.choice(turns))
        pydirectinput.moveTo(x+turn_var, y)
        pydirectinput.press(move_var)

    pydirectinput.keyUp('w')

def mining(dur=5):

    x = int(pydirectinput.position()[0])
    y = int(pydirectinput.size()[1])

    # tilt down to point direction towards ground
    pydirectinput.moveTo(x, y)

    # start mining
    pydirectinput.mouseDown(button='left')
    time.sleep(dur)
    pydirectinput.mouseUp(button='left')

def building(dur=5):
    pydirectinput.keyDown('1')
    pydirectinput.keyDown('s')
    pydirectinput.mouseDown(button='right')
    time.sleep(dur)
    pydirectinput.keyUp('s')
    pydirectinput.mouseUp(button='right')

def stationary(dur=5):
    # Keeps at stationary position and don't do anything
    time.sleep(dur)
    

def main():
    
    """ Alt-tab to switch to Minecraft tab after executing the program """
    duration = 1000  # milliseconds
    freq = 440  # Hz

    # delay needed for switching tabs
    time.sleep(2)
    winsound.Beep(freq, duration)

    x_size = int(pydirectinput.size()[0])
    y_size = int(pydirectinput.size()[1])
    print('Size of the window: {}'.format(pydirectinput.size()))
    
    x = int(pydirectinput.position()[0])
    y = int(pydirectinput.position()[1])
    curr_cur()

    """ Run any functions to activate movements in Minecraft"""
    
    # wandering()
    # mining()
    # building()
    # stationary

    # To determine if program finished executing
    winsound.Beep(freq, duration)

    

    """ real-time cursor coordinates """
    # def coords():
    # print('Press Ctrl-C to quit.')
    # try:
    #     while True:
    #         x, y = pydirectinput.position()
    #         positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
    #         print(positionStr, end='')
    #         print('\b' * len(positionStr), end='', flush=True)
    # except KeyboardInterrupt:
    #     print('\n')

