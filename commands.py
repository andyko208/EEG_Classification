import pyautogui
import pydirectinput

import random
import time
import winsound
import sys

""" Always centers cursor at x: 1280 y: 782"""

def curr_cur():
    print('Current cursor x: {} y: {}'.format(pydirectinput.position()[0], pydirectinput.position()[1]))
    # print('Current cursor x: {} y: {}'.format(pyautogui.position()[0], pyautogui.position()[1]))

duration = 1000  # milliseconds
freq = 440  # Hz

x_size = int(pydirectinput.size()[0])
y_size = int(pydirectinput.size()[1])
print('Size of the window: {}'.format(pydirectinput.size()))

time.sleep(3)

x = int(pydirectinput.position()[0]+200)
y = int(pydirectinput.position()[1])

print('Moving to x: {} y:{}'.format(x, y))

# pydirectinput.moveTo(x, y)
curr_cur()
winsound.Beep(freq, duration)


""" real-time cursor coordinates"""
# import pyautogui, sys
# print('Press Ctrl-C to quit.')
# try:
#     while True:
#         x, y = pyautogui.position()
#         positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
#         print(positionStr, end='')
#         print('\b' * len(positionStr), end='', flush=True)
# except KeyboardInterrupt:
#     print('\n')

def wandering():
    moves = ('a', 'd', 'space')
    try:
        t_init = time.time()
        dur = 5
        while (time.time() - t_init) < dur:
            pydirectinput.keyDown('w')
            move_var = random.choice(moves)
            x = int((x_size / 2) + ((x_size / 100) * 5))
            y = int((y_size / 2) - ((y_size / 100) * 5))
            pydirectinput.moveTo(x, y)
            pydirectinput.moveTo(x, y)
            pydirectinput.press(move_var)
            # if state != 'wandering':
            #     break
    except KeyboardInterrupt:
        pass

def mining():
    t_init = time.time()
    dur = 3
    while (time.time() - t_init) < dur:
        pydirectinput.mouseDown(button='left')
    # if state != 'mining':
    #     break
    pydirectinput.mouseUp(button='left')

if __name__ == "__main__":
    mining()

