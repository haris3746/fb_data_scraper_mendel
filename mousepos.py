import time
import pyautogui

time.sleep(10)
screen_size=pyautogui.size()
print("screen_size ", screen_size)
pyautogui.moveTo(220, 630, duration = 1)
print(pyautogui.position())

time.sleep(10)
pyautogui.click()

