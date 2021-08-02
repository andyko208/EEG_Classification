import pyautogui
import pyautogui

import random
import time
import winsound
import sys

""" Always centers cursor at x: 1280 y: 782"""

def curr_cur():
    print('Current cursor x: {} y: {}'.format(pyautogui.position()[0], pyautogui.position()[1]))
    # print('Current cursor x: {} y: {}'.format(pyautogui.position()[0], pyautogui.position()[1]))

duration = 1000  # milliseconds
freq = 440  # Hz

x_size = int(pyautogui.size()[0])
y_size = int(pyautogui.size()[1])
print('Size of the window: {}'.format(pyautogui.size()))

time.sleep(3)



# print('Moving to x: {} y:{}'.format(x, y))

# pyautogui.moveTo(x, y)
curr_cur()
winsound.Beep(freq, duration)

def wandering():

    
    moves = ('a', 'd', 'space')
    turns = (150, -150)
    t_init = time.time()
    dur = 10
    while (time.time() - t_init) < dur:
        pyautogui.keyDown('w')
        move_var = random.choice(moves)
        x = int(pyautogui.position()[0])
        y = int(pyautogui.position()[1])
        turn_var = int(random.choice(turns))
        pyautogui.moveTo(x+turn_var, y)
        pyautogui.press(move_var)
        # curr_cur()
        # if state != 'wandering':
        #     break
    pyautogui.keyUp('w')

def mining():
    t_init = time.time()
    dur = 5
    while (time.time() - t_init) < dur:
        # pyautogui.
        pyautogui.mouseDown(button='left')
    # if state != 'mining':
    #     break
    pyautogui.mouseUp(button='left')

if __name__ == "__main__":
    # mining()
    # wandering()
    x = int(pyautogui.position()[0])
    # y = int(pyautogui.position()[1]+250)
    y = int(y_size)
    pyautogui.moveTo(x, y)
    

    """ real-time cursor coordinates"""
    # print('Press Ctrl-C to quit.')
    # try:
    #     while True:
    #         x, y = pyautogui.position()
    #         positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
    #         print(positionStr, end='')
    #         print('\b' * len(positionStr), end='', flush=True)
    # except KeyboardInterrupt:
    #     print('\n')

