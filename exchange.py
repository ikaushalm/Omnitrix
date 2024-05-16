import string
from time import sleep
import pyautogui
import pytesseract
from PIL import ImageGrab
from PIL import Image
import random
import numpy as np
import re
import cv2

function_one=1
function_change=1
last_value=None
loss_count=0
loop_count=0
repeat_count=1



def betonA():
    pyautogui.click(x=850, y=800) 

def betonB():
    pyautogui.click(x=1050,y= 800)

   


# get Teserect Executable Location
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
#to take screen out of this ide
target_amt=pyautogui.prompt(text="",title="Enter the Openning balance")
sleep(2)

def function_one():
    print("Function One called")

def function_two():
    print("Function Two called")

# # Function to handle mouse events
# def draw_rectangle(event, x, y, flags, param):
#     global drawing, top_left, bottom_right

#     if event == cv2.EVENT_LBUTTONDOWN:
#         drawing = True
#         top_left = (x, y)

#     elif event == cv2.EVENT_MOUSEMOVE:
#         if drawing:
#             bottom_right = (x, y)

#     elif event == cv2.EVENT_LBUTTONUP:
#         drawing = False
#         bottom_right = (x, y)
#         cv2.rectangle(screen_copy, top_left, bottom_right, (0, 255, 0), 2)
#         bounding_boxes.append((top_left, bottom_right))

# # Capture the screen
# screen = pyautogui.screenshot()
# screen = np.array(screen)

# # Make a copy for drawing
# screen_copy = screen.copy()

# # Initialize variables
# drawing = False
# top_left = None
# bottom_right = None
# bounding_boxes = []

# # Create a window and set mouse callback
# cv2.namedWindow('Select Bounding Boxes')
# cv2.setMouseCallback('Select Bounding Boxes', draw_rectangle)

# while True:
#     cv2.imshow('Select Bounding Boxes', screen_copy)
#     key = cv2.waitKey(1) & 0xFF

#     # Press 'c' to clear selection
#     if key == ord('c'):
#         screen_copy = screen.copy()
#         bounding_boxes.clear()

#     # Press 'q' to quit selection
#     elif key == ord('q'):
#         break

# # Release resources and close windows
# cv2.destroyAllWindows()

# # Print selected bounding box coordinates
# print("Selected Bounding Box Coordinates:")
# for box in bounding_boxes:
#     print("Top-left:", box[0])
#     print("Bottom-right:", box[1])

# Define a function to set the global variable
def set_last_value(value):
    global last_value
    last_value = value


starting_value = ImageGrab.grab(bbox=(1109, 131, 1239, 152))
txt = pytesseract.image_to_string(starting_value,config='--psm 6')
print(txt)
print(len(txt))
try:                                                                  
    startingvaluefinal=float(txt)
    target_amt_final=float(target_amt)
    print(target_amt)
    while startingvaluefinal<target_amt_final:
        print('inside function')
        try:
            lock_check = pyautogui.locateOnScreen("placeyourbets.png", confidence=0.8)
            print(lock_check)
            strLockcheck = str(lock_check)
            print(len(strLockcheck))
            
        except:
            print("unable to find lock")
            strLockcheck=''

        if(len(strLockcheck)==44) :
            sleep(2)
            pyautogui.click(1150,135)
            sleep(2)
            current_value = ImageGrab.grab(bbox=(1109, 131, 1239, 152))
            current_txt = pytesseract.image_to_string(current_value,config='--psm 6')
            current_value_final=float(current_txt)
            if(loop_count!=0):
                print(last_value)
                print(current_value_final)
                if(last_value>current_value_final):
                    print('inside true loop')
                    loss_count=loss_count+1
                    if loss_count==1:
                        repeat_count=2
                    elif loss_count==2: 
                        repeat_count=4
                    elif loss_count==3:
                        repeat_count=8
                    elif loss_count==4:
                        repeat_count=16
                    elif loss_count==5:
                        repeat_count=32
                    elif loss_count==6:
                        repeat_count=64
                    elif loss_count==7:
                        repeat_count=128
                    else:
                        repeat_count=loss_count*2

                    print('printing loss count')
                    print(loss_count)
                else:
                    repeat_count=1
                    loss_count=0
            try:
                print('repeat_count')
                print(repeat_count)
                if function_change==1:  # Call function_one() twice for every even iteration
                    for _ in range(repeat_count):
                        betonB()
                    function_change=2
                    pyautogui.click(1150,135)
                    sleep(2)
                    last_value_pic = ImageGrab.grab(bbox=(1109, 131, 1239, 152))
                    last_value_txt = pytesseract.image_to_string(last_value_pic,config='--psm 6')
                    set_last_value(float(last_value_txt))
                    
                elif function_change==2:  # Call function_one() twice for every even iteration
                    for _ in range(repeat_count):
                         betonB()
                    function_change=3
                    pyautogui.click(1150,135)
                    sleep(2)                   
                    last_value_pic = ImageGrab.grab(bbox=(1109, 131, 1239, 152))
                    last_value_txt = pytesseract.image_to_string(last_value_pic,config='--psm 6')
                    set_last_value(float(last_value_txt))
                elif function_change==3:  # Call function_one() twice for every even iteration
                    for _ in range(repeat_count):
                        betonA()
                    function_change=4
                    pyautogui.click(1150,135)
                    sleep(2)
                    last_value_pic = ImageGrab.grab(bbox=(1109, 131, 1239, 152))
                    last_value_txt = pytesseract.image_to_string(last_value_pic,config='--psm 6')
                    set_last_value(float(last_value_txt))
                elif function_change==4:  # Call function_one() twice for every even iteration
                    for _ in range(repeat_count):
                        betonA()
                    function_change=1
                    pyautogui.click(1150,135)
                    sleep(2)
                    last_value_pic = ImageGrab.grab(bbox=(1109, 131, 1239, 152))
                    last_value_txt = pytesseract.image_to_string(last_value_pic,config='--psm 6')
                    set_last_value(float(last_value_txt))
                loop_count=loop_count+1
                starting_value = ImageGrab.grab(bbox=(1109, 131, 1239, 152))
                txt = pytesseract.image_to_string(starting_value,config='--psm 6')
                startingvaluefinal=float(txt)
                sleep(28)    
            except:
                print("Unable to get the bet history")
        else:
            print("Unable to get the lock")
except:
    print('Pls go to the  original screen')



