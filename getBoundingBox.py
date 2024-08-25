from time import sleep
import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab

# Scaling factor
SCALE_FACTOR = 0.5

sleep(3)

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
        # Draw rectangle on scaled-down image
        cv2.rectangle(screen_copy, top_left, bottom_right, (0, 255, 0), 2)
        # Convert coordinates to the full-size image scale
        full_top_left = (int(top_left[0] / SCALE_FACTOR), int(top_left[1] / SCALE_FACTOR))
        full_bottom_right = (int(bottom_right[0] / SCALE_FACTOR), int(bottom_right[1] / SCALE_FACTOR))
        bounding_boxes.append((full_top_left, full_bottom_right))

def capture_screen():
    try:
        # Use ImageGrab from PIL for capturing the screen
        screen = ImageGrab.grab()
        return np.array(screen)
    except Exception as e:
        print(f"Error capturing screen: {e}")
        exit()

# Capture the screen
screen = capture_screen()

# Scale down the screenshot
small_screen = cv2.resize(screen, (0, 0), fx=SCALE_FACTOR, fy=SCALE_FACTOR)

# Make a copy for drawing
screen_copy = small_screen.copy()

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
        screen_copy = small_screen.copy()
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
