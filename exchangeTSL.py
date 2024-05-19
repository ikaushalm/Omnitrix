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

from twilio.rest import Client

# Your Twilio Account SID and Auth Token
account_sid = 'ACcf5c43d3ca76cbd9cc51b4b2ae1dff6c'
auth_token = '1809f844d96bbe6bc57906ead628f039'

# Create a Twilio client
client = Client(account_sid, auth_token)

# Your Twilio phone number (obtained from Twilio)
from_phone = '+14144859675'

# The recipient's phone number
to_phone = '+917786868782'




function_one=1
function_change=1
last_value=None
loss_count=0
loop_count=0
repeat_count=1


at_last_value=None
at_loss_count=0
at_loop_count=0
at_repeat_count=1
at_function_change=1



def betonA():
    # 567, 600
    pyautogui.click(x=600,y= 600)

def betonB():
    # 700, 600
    pyautogui.click(x=740,y= 600)

arrhistory=[]

def add_to_fixed_length_array(arr, new_value):
   
    arr.append(new_value)
    
    # If the length of the array exceeds the fixed length, remove the oldest element
    if len(arr) > 10:
        arr.pop(0)  # Remove the oldest element
    
    return arr



def extract_numbers(text):
     # Define the regex pattern to match numbers and decimal points
    pattern = r'\d+(\.\d+)?'
    # Use re.search to find the first match in the text
    match = re.search(pattern, text)
    if match:
        # Extract the matched number string
        number_str = match.group()
        # Convert the matched string to a float
        number = float(number_str)
        return number
    else:
        return None  # Return None if no number is found

# get Teserect Executable Location
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
#to take screen out of this ide
target_amt=pyautogui.prompt(text="",title="Enter your target")
sleep(2)
at_max_loss=pyautogui.prompt(text="This will hit when your target is already completed",title="Enter your maximum loss in rupee")
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


def set_last_value_at(value):
    global at_last_value
    at_last_value = value

starting_value = ImageGrab.grab(bbox=(735, 104, 815, 120))
txt = extract_numbers(pytesseract.image_to_string(starting_value,config='--psm 6'))
print(txt)
flag=False
targetyes=0

try:    
    # pyautogui.click(x=607, y=640)                                                               
    startingvaluefinal=float(txt)
    target_amt_final=float(target_amt)
    print(startingvaluefinal)
    print(target_amt_final)
    while True:
        while startingvaluefinal>target_amt_final: 
            print('getting ready for trailling stop loss')
            try:
                at_lock_check = pyautogui.locateOnScreen("placeyourbets.png", confidence=0.8)
                print(at_lock_check)
                at_strLockcheck = str(at_lock_check)
                print(len(at_strLockcheck))
                if targetyes==0:
                    # The message you want to send
                    message_body = "previous Target Achieved: " + str(target_amt_final) + " Getting ready for TSL"


                    # Send the SMS
                    message = client.messages.create(
                    body=message_body,
                    from_=from_phone,
                    to=to_phone
                    )
                    targetyes=targetyes+1

               

            except:
                print("unable to find lock")
                at_strLockcheck=''
            if(len(at_strLockcheck)==43) :
                sleep(2)
                pyautogui.click(795,110)
                sleep(2)
                at_current_value = ImageGrab.grab(bbox=(735, 104, 815, 120))
                at_current_txt = pytesseract.image_to_string(at_current_value,config='--psm 6')
                at_current_value_final=float(extract_numbers(at_current_txt))
                if at_loop_count!=0:
                    at_loss_limit=max(arrhistory)-float(at_max_loss)
                    if at_current_value_final<at_loss_limit:
                        print('setting break flag to true')
                        # print("last value " + arrhistory[-1] +"maximum loss value as per tsl"+at_loss_limit )
                        flag = True
                        message_body = "Trailing stop Loss hit:"+str(at_loss_limit) + "Programm is closing"

                        # Send the SMS
                        message = client.messages.create(
                        body=message_body,
                        from_=from_phone,
                        to=to_phone
                        )

                        break

                if(at_loop_count!=0):
                    print(at_last_value)
                    print(at_current_value_final)
                    if(at_last_value>at_current_value_final):
                        print('inside true loop')
                        at_loss_count=at_loss_count+1
                        if at_loss_count==1:
                            at_repeat_count=2
                        elif at_loss_count==2: 
                            at_repeat_count=4
                        elif at_loss_count==3:
                            at_repeat_count=8
                        elif at_loss_count==4:
                            at_repeat_count=16
                        elif at_loss_count==5:
                            at_repeat_count=32
                        elif at_loss_count==6:
                            at_repeat_count=64
                        elif at_loss_count==7:
                            at_repeat_count=128
                        else:
                            at_repeat_count=at_loss_count*2

                        print('printing loss count')
                        print(at_loss_count)
                    else:
                        at_repeat_count=1
                        at_loss_count=0
                try:
                    print('at_repeat_count')
                    print(at_repeat_count)
                    if at_loss_count>=6:
                        #taking screen shots for maximum loss for better understanding of the data
                        # Top-left: (315, 563)
                        # Bottom-right: (502, 618)
                        pic = ImageGrab.grab(bbox=(315, 563, 502, 618))
                        pic.save("screenshot.png")
                                            

                    if at_function_change==1:  # Call function_one() twice for every even iteration
                        for _ in range(at_repeat_count):
                            betonB()
                        at_function_change=2
                        pyautogui.click(795,110)
                        sleep(2)
                        last_value_pic = ImageGrab.grab(bbox=(735, 104, 815, 120))
                        last_value_txt = pytesseract.image_to_string(last_value_pic,config='--psm 6')
                        set_last_value_at(float(extract_numbers(last_value_txt)))
                        add_to_fixed_length_array(arrhistory, extract_numbers(last_value_txt))
                        
                    elif at_function_change==2:  # Call function_one() twice for every even iteration
                        for _ in range(at_repeat_count):
                            betonB()
                        at_function_change=3
                        pyautogui.click(795,110)
                        sleep(2)                   
                        last_value_pic = ImageGrab.grab(bbox=(735, 104, 815, 120))
                        last_value_txt = pytesseract.image_to_string(last_value_pic,config='--psm 6')
                        set_last_value_at(float(extract_numbers(last_value_txt)))
                        add_to_fixed_length_array(arrhistory, extract_numbers(last_value_txt))
                    elif at_function_change==3:  # Call function_one() twice for every even iteration
                        for _ in range(at_repeat_count):
                            betonA()
                        at_function_change=4
                        pyautogui.click(795,110)
                        sleep(2)
                        last_value_pic = ImageGrab.grab(bbox=(735, 104, 815, 120))
                        last_value_txt = pytesseract.image_to_string(last_value_pic,config='--psm 6')
                        set_last_value_at(float(extract_numbers(last_value_txt)))
                        add_to_fixed_length_array(arrhistory, extract_numbers(last_value_txt))
                    elif at_function_change==4:  # Call function_one() twice for every even iteration
                        for _ in range(at_repeat_count):
                            betonA()
                        at_function_change=1
                        pyautogui.click(795,110)
                        sleep(2)
                        last_value_pic = ImageGrab.grab(bbox=(735, 104, 815, 120))
                        last_value_txt = pytesseract.image_to_string(last_value_pic,config='--psm 6')
                        set_last_value_at(float(extract_numbers(last_value_txt)))
                        add_to_fixed_length_array(arrhistory, extract_numbers(last_value_txt))
                    at_loop_count=at_loop_count+1
                 
                    sleep(28)    
                except:
                    print("Unable to get the bet history")
            else:
                print("Unable to get the lock")
        if flag:
            print("Your trailing stop loss is hit ")
            break  # Break the outer loop if the flag is True
            
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
            if(len(strLockcheck)==43) :
                sleep(2)
                pyautogui.click(795,110)
                sleep(2)
                current_value = ImageGrab.grab(bbox=(735, 104, 815, 120))
                current_txt = pytesseract.image_to_string(current_value,config='--psm 6')
                current_value_final=float(extract_numbers(current_txt))
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
                    if loss_count>=6:
                        #taking screen shots for maximum loss for better understanding of the data
                        # Top-left: (315, 563)
                        # Bottom-right: (502, 618)
                        pic = ImageGrab.grab(bbox=(315, 563, 502, 618))
                        pic.save("screenshot.png")
                                            

                    if function_change==1:  # Call function_one() twice for every even iteration
                        for _ in range(repeat_count):
                            betonB()
                        function_change=2
                        pyautogui.click(795,110)
                        sleep(2)
                        last_value_pic = ImageGrab.grab(bbox=(735, 104, 815, 120))
                        last_value_txt = pytesseract.image_to_string(last_value_pic,config='--psm 6')
                        set_last_value(float(extract_numbers(last_value_txt)))
                        
                    elif function_change==2:  # Call function_one() twice for every even iteration
                        for _ in range(repeat_count):
                            betonB()
                        function_change=3
                        pyautogui.click(795,110)
                        sleep(2)                   
                        last_value_pic = ImageGrab.grab(bbox=(735, 104, 815, 120))
                        last_value_txt = pytesseract.image_to_string(last_value_pic,config='--psm 6')
                        set_last_value(float(extract_numbers(last_value_txt)))
                    elif function_change==3:  # Call function_one() twice for every even iteration
                        for _ in range(repeat_count):
                            betonA()
                        function_change=4
                        pyautogui.click(795,110)
                        sleep(2)
                        last_value_pic = ImageGrab.grab(bbox=(735, 104, 815, 120))
                        last_value_txt = pytesseract.image_to_string(last_value_pic,config='--psm 6')
                        set_last_value(float(extract_numbers(last_value_txt)))
                    elif function_change==4:  # Call function_one() twice for every even iteration
                        for _ in range(repeat_count):
                            betonA()
                        function_change=1
                        pyautogui.click(795,110)
                        sleep(2)
                        last_value_pic = ImageGrab.grab(bbox=(735, 104, 815, 120))
                        last_value_txt = pytesseract.image_to_string(last_value_pic,config='--psm 6')
                        set_last_value(float(extract_numbers(last_value_txt)))
                    loop_count=loop_count+1
                    starting_value = ImageGrab.grab(bbox=(735, 104, 815, 120))
                    txt = pytesseract.image_to_string(starting_value,config='--psm 6')
                    startingvaluefinal=float(extract_numbers(txt))
                    sleep(20)    
                except:
                    print("Unable to get the bet history")
            else:
                print("Unable to get the lock")
except:
    print('Pls go to the  original screen')



