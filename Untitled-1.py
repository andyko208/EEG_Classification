import pyautogui
import pydirectinput
# import keyboard

import random
import time
import winsound
import pynput
# from pywinauto import keyboard

duration = 1000  # milliseconds
freq = 440  # Hz

time.sleep(5)

# pydirectinput.click()
# pydirectinput.press('t')
# pydirectinput.click(button='right')
# pydirectinput.mouseUp(150, 250, button='right', duration=0.5)


x = pydirectinput.size()[0]
y = pydirectinput.size()[1]

print(x)
print(y)

""" (x = horizontal, y = vertical) """
go_by = 450

pydirectinput.moveTo(int(x/2), y)
pydirectinput.moveTo(int(x/2), y)
winsound.Beep(freq, duration)
print('The current pointer position is {0}'.format(pydirectinput.position()))
time.sleep(2)
# pydirectinput.moveTo(int(x/2), int(y/2))
pydirectinput.moveTo(150, 320)
print('The current pointer position is {0}'.format(pydirectinput.position()))
# time.sleep(0.5)
# pydirectinput.moveTo(980, 350 + go_by)
# pydirectinput.click()
# print('The current pointer position is {0}'.format(pydirectinput.position()))

# pydirectinput.mouseUp(150, 250, button='right', duration=0.5)



# mouse.move(1036, 382)w
winsound.Beep(freq, duration)



# winsound.Beep(freq, duration)

# print(pyautogui.size())
# print(pyautogui.onScreen(x, y))

# rand_interval = random.randint()