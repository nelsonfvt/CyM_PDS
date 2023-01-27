import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def grab_frameRGB(cap):
    ret,frame = cap.read()
    return cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

def grab_frameBGR(cap):
    ret,frame = cap.read()
    return frame

print("[INFO] starting camera...")
cap1 = cv2.VideoCapture(0)
if not cap1.isOpened():
    print("No se puede abrir camara 0")
    exit()

ax1 = plt.subplot(1,2,1)
plt.title('Raw capture')
ax2 = plt.subplot(1,2,2)
plt.title('Color corrected')

ret, frame = cap1.read()

im1 = ax1.imshow(frame)
im2 = ax2.imshow(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))

def update(i):
    im1.set_data(grab_frameBGR(cap1))
    im2.set_data(grab_frameRGB(cap1))

ani = FuncAnimation(plt.gcf(), update, interval=50)
plt.show()