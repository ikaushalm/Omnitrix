from time import sleep
import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab

sleep(3)
# Function to handle mouse events
def draw_rectangle(event, x, y, flags, param):
    global drawing, top_left, bottom_right

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        top_left = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            bottom_right = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        bottom_right = (x, y)
        cv2.rectangle(screen_copy, top_left, bottom_right, (0, 255, 0), 2)
        bounding_boxes.append((top_left, bottom_right))

# Capture the screen
screen = pyautogui.screenshot()
screen = np.array(screen)

# Make a copy for drawing
screen_copy = screen.copy()

# Initialize variables
drawing = False
top_left = None
bottom_right = None
bounding_boxes = []

# Create a window and set mouse callback
cv2.namedWindow('Select Bounding Boxes')
cv2.setMouseCallback('Select Bounding Boxes', draw_rectangle)

while True:
    cv2.imshow('Select Bounding Boxes', screen_copy)
    key = cv2.waitKey(1) & 0xFF

    # Press 'c' to clear selection
    if key == ord('c'):
        screen_copy = screen.copy()
        bounding_boxes.clear()

    # Press 'q' to quit selection
    elif key == ord('q'):
        break

# Release resources and close windows
cv2.destroyAllWindows()

# Print selected bounding box coordinates
print("Selected Bounding Box Coordinates:")
for box in bounding_boxes:
    print("Top-left:", box[0])
    print("Bottom-right:", box[1])
