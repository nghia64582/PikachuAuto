import numpy as np
from time import *
import cv2
import pyautogui as pa

start=time()
pa.PAUSE=0
for i in range(1000):
	pa.click()
print(time()-start)