import base64
import math
import random
import subprocess
import pyperclip
import pyautogui
import time
import random
import math
from time import sleep
import re
import logging
import winsound
import os
from datetime import datetime
import time 
import csv
import platform
import threading
from PIL import ImageGrab
import pytesseract
from PIL import Image

# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------
# --------------Configuration Files------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------



screenWidth, screenHeight = pyautogui.size()

global fibo_series
fibo_series=[1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89,144]
# A--axis for BetOnA---------------------------------------
# 850, 800, 20 -for Santosh Bhaiya Machine-----------------

relative_Ax = 850 / 1920  # Relative position on X-axis
relative_Ay = 800 / 1080   # Relative position on Y-axis
A_x = screenWidth*relative_Ax
A_y = screenHeight*relative_Ay

# radius is common for moving cursor in round--------------
# ---------------------------------------------------------
moving_r = 20 
# ----------------------------------------------------------


# B--axis for BetOnB---------------------------------------
# 1050, 800, 20-for Santosh Bhaiya Machine-----------------


relative_Bx = 1050 / 1920  # Relative position on X-axis
relative_By = 800 / 1080   # Relative position on Y-axis

B_x = screenWidth*relative_Bx
B_y = screenHeight*relative_By

# ---------------------------------------------------------
# get_text_at_position
# 1150,135,0.5 -for Santosh Bhaiya Machine-----------------

relative_x = 1115 / 1920  # Relative position on X-axis
relative_y = 138 / 1080   # Relative position on Y-axis

textat_x= screenWidth*relative_x
textat_y=screenHeight*relative_y
moving_delay=0.5
# ---------------------------------------------------------
# Baseuri
# Your base64 encoded string
encoded_string = "aW5kaWEuMXhiZXQuY29tLw=="
# Decode the base64 string
decoded_bytes = base64.b64decode(encoded_string)
BaseUrl = decoded_bytes.decode('utf-8')
# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------


Bethistory=[]
function_one=1
function_change=1
last_value=None
loss_count=0
win_count=0
loop_count=0
repeat_count=1
bet_count=0
startingvaluefinal=0
isFifth=False
BestStrategy='B'

# Define the global variable
betted_on = None

def set_betted_on(value):
    global betted_on
    betted_on = value

def compare_betted_on(value):
    global betted_on
    if betted_on == value:
        return True
    else:
        return False




pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# Load the image
image_path = 'fifthtext.png'  # Replace with your image path

def extract_characters_from_image(image_path):
    # Load the image
    img = Image.open(image_path)

    # Convert image to RGB and extract pixels
 
    # Fallback to OCR if no colors were detected
    text = pytesseract.image_to_string(img, config='--psm 6')
    print(txt)
    filtered_text = ''.join(c for c in text if c in 'AB')
    return filtered_text[-1] if filtered_text else None
    


def extract_maxcount_from_image(image_path):
    # Load the image
    img = Image.open(image_path)
    # Fallback to OCR if no colors were detected
    text = pytesseract.image_to_string(img, config='--psm 6')
    filtered_text = ''.join(c for c in text if c in 'AB')
    if filtered_text:
        return max(filtered_text, key=filtered_text.count)  # Return the character with the highest count from OCR
    else:
        return None

# Define the log directory and ensure it exists
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Generate a timestamp for the log filename
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
log_filename = f'{log_dir}/bot_{timestamp}.log'

# Set up basic configuration for logging
logging.basicConfig(filename=log_filename, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')


# CSV file setup
csv_filename = f'{log_dir}/bot_data_{timestamp}.csv'
csv_headers = ['Time','Betted On', 'CurrentValue', 'TargetAmt', 'Losscount', 'Wincount']

# Initialize CSV file with headers if it does not exist
if not os.path.isfile(csv_filename):
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_headers)

def write_to_csv(time,betted_on, current_value, target_amt, losscount, wincount):
    """Write data to the CSV file."""
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([time,betted_on, current_value, target_amt, losscount, wincount])

def play_alarm():
    """Play an alarm sound."""
    frequency = 1000  # Frequency in Hz
    duration = 2000   # Duration in milliseconds
    winsound.Beep(frequency, duration)




def close_chrome_tabs():
    """Close all Chrome tabs."""
    try:
        if platform.system() == 'Windows':
            # Close Chrome via taskkill
            subprocess.call(['taskkill', '/F', '/IM', 'chrome.exe'])
        else:
            print("Unsupported OS")
    except Exception as e:
        logging.error(f"An error occurred while closing Chrome tabs: {e}", exc_info=True)

def shutdown_system():
    """Shut down the system."""
    try:
        if platform.system() == 'Windows':
            subprocess.call(['shutdown', '/s', '/t', '0'])
        else:
            print("Unsupported OS")
    except Exception as e:
        logging.error(f"An error occurred while shutting down the system: {e}", exc_info=True)

def open_incognito_website(url):
    # Determine the platform and path to Chrome executable
    if platform.system() == "Windows":
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    elif platform.system() == "Darwin":  # macOS
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    elif platform.system() == "Linux":
        chrome_path = "/usr/bin/google-chrome"
    else:
        raise OSError("Unsupported operating system")

    # Prepare the command for launching Chrome in incognito mode
    command = [chrome_path, '--incognito', url]

    # Launch Chrome in incognito mode with the specified URL
    try:
        subprocess.run(command, check=True)
    except FileNotFoundError:
        print(f"Error: Chrome executable not found at {chrome_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")




def move_cursor_in_random_circles(center_x, center_y, radius, duration=6):
    """Move the cursor in random circles around the given center point for the specified duration with human-like imperfections.
    Returns the final x and y coordinates of the cursor."""
    
    screen_width, screen_height = pyautogui.size()  # Get screen dimensions
    start_time = time.time()
    
    # Initialize final position variables
    final_x = center_x
    final_y = center_y
    
    while time.time() - start_time < duration:
        num_steps = random.randint(15, 25)  # More steps for smoother circles
        for step in range(num_steps):
            angle = 2 * math.pi * step / num_steps
            
            # Introduce slight random deviations
            deviation_angle = random.uniform(-0.2, 0.2)
            deviation_radius = random.uniform(-5, 5)
            x = center_x + (radius + deviation_radius) * math.cos(angle + deviation_angle)
            y = center_y + (radius + deviation_radius) * math.sin(angle + deviation_angle)
            
            # Ensure cursor stays within screen bounds
            x = max(0, min(screen_width - 1, x))
            y = max(0, min(screen_height - 1, y))
            
            # Move cursor with variable speed
            move_duration = random.uniform(0.1, 0.3)  # Slightly variable durations
            pyautogui.moveTo(x, y, duration=move_duration)
            
            # Update final position
            final_x, final_y = x, y
            
            # Add a variable delay for more natural movement
            time.sleep(random.uniform(0.05, 0.15))
        
        # Randomly adjust radius and center for the next circle
        radius = max(5, radius + random.uniform(-10, 10))  # Prevent radius from going too small
        center_x = max(0, min(screen_width - 1, center_x + random.uniform(-20, 20)))  # Adjust center with bounds check
        center_y = max(0, min(screen_height - 1, center_y + random.uniform(-20, 20)))  # Adjust center with bounds check
    
    # Return the final x and y coordinates
    return final_x, final_y


def betonA(no_click):
    # pyautogui.click(x=600,y= 600,clicks=no_click)
    final_x, final_y =move_cursor_in_random_circles(A_x, A_y, moving_r)  # Move cursor in random circles around the betting point
    # sleep(1)  # Short delay to mimic human behavior
    pyautogui.click(x=final_x, y=final_y,clicks=no_click)
    set_betted_on('A')
    # logging.info("Betting on A --Current value:{starting_value_final} Target Value:{target_amt}  Loss Count: {loss_count} Win Count:{win_count} Repeat_count:{repeat_count}")
    logging.info(f"A,{startingvaluefinal},{target_amt},{loss_count},{win_count}")
    write_to_csv(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'A', startingvaluefinal, target_amt, loss_count, win_count)



def betonB(no_click):
    # pyautogui.click(x=740,y= 600,clicks=no_click)
    """Perform betting action on B."""
    final_x, final_y =move_cursor_in_random_circles(B_x,B_y,moving_r)  # Move cursor in random circles around the betting point
    # sleep(1)  # Short delay to mimic human behavior
    pyautogui.click(x=final_x,y=final_y,clicks=no_click)

    set_betted_on('B')
    # logging.info("Betting on B --Loss Count: {loss_count} Win Count:{win_count} Repeat_count:{repeat_count}")
    logging.info(f"B,{startingvaluefinal},{target_amt},{loss_count},{win_count}")
    write_to_csv(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'B', startingvaluefinal, target_amt, loss_count, win_count)


# Extracting numbers from text
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

thread = threading.Thread(target=open_incognito_website(url=BaseUrl))
thread.start()
thread.join()

#to take screen out of this ide
target_amt=pyautogui.prompt(text="",title="Enter your target")
sleep(2)




Target_break=pyautogui.prompt(text="",title="Enter your Multiple Amount")
sleep(2)



def set_last_value(value):
    global last_value
    last_value = value

def set_new_target_val(value):
    global new_target
    new_target = value

def set_last_value_at(value):
    global at_last_value
    at_last_value = value

def get_text_at_position(x, y, duration=0.01):
    """
    Move the cursor to the given position (x, y), select the text by double-clicking, 
    and return the copied text.
    
    Parameters:
    x (int): The x-coordinate of the position.
    y (int): The y-coordinate of the position.
    duration (float): The duration for cursor movement (optional).
    
    Returns:
    str: The text copied from the specified position.
    """
    # Move the cursor to the specified location
    pyautogui.moveTo(x, y, duration=duration)
    
    # Double-click to select the text
    pyautogui.doubleClick()
    
    # Give a short delay to ensure text selection and copying
    time.sleep(1)
    
    # Simulate pressing the copy keyboard shortcut (Ctrl+C on Windows/Linux, Command+C on macOS)
    pyautogui.hotkey('ctrl', 'c')  # Use 'command', 'c' on macOS
    
    # Give a short delay to ensure the clipboard is updated
    time.sleep(0.5)
    
    # Retrieve the text from the clipboard
    copied_text = pyperclip.paste()
    
    return copied_text



def add_to_fixed_length_array(arr, new_value):
    arr.append(new_value)
    # If the length of the array exceeds the fixed length, remove the oldest element
    if len(arr) > 4:
        arr.pop(0)  # Remove the oldest element
    return arr

# To check values are equal
def all_equal(arr):
    # Check if the length of the array is less than 4
    if len(arr) < 4:
        return False
    # Check if all elements are equal
    return all(x == arr[0] for x in arr)



pyautogui.click(textat_x,textat_y)
sleep(2)

starting_value = get_text_at_position(textat_x,textat_y,moving_delay)
txt = extract_numbers(starting_value)
flag=False
targetyes=0

try:    
    # pyautogui.click(x=607, y=640)                                                               
    startingvaluefinal=float(txt)
    Target_break_final=float(Target_break)
    set_new_target_val(startingvaluefinal+Target_break_final)
    function_change=1
    target_amt_final=float(target_amt)
    logging.info(f"Starting value: {startingvaluefinal}")
    logging.info(f"Target amount: {target_amt}")
    logging.info("Betted On,CurrentValue,TargetAmt,Losscount,Wincount")
    while True:             
        while startingvaluefinal<target_amt_final:
            if(loop_count!=0):
                current_txt = get_text_at_position(textat_x,textat_y,moving_delay)
                startingvaluefinal=float(extract_numbers(current_txt))
            print(f'new target {new_target}')
            print(f'Starting Value final {startingvaluefinal}')
            if(all_equal(Bethistory)):
                set_new_target_val(startingvaluefinal+Target_break_final)
            else:
                if(startingvaluefinal>new_target):

                    print(f'New Target Achieved {new_target}')
                    set_new_target_val(startingvaluefinal+Target_break_final)
                    #reset values
                    Bethistory=[]
                    function_one=1
                    function_change=1
                    loss_count=0
                    win_count=0
                    repeat_count=1
                    isFifth=False
                    sleep_test=0
                    
                    next_multiple_of_5 = (bet_count + 4) // 5 * 5
                    loop_condition=next_multiple_of_5-bet_count
                    while(sleep_test<loop_condition):

                        try:
                            sleepstrLockcheck = pyautogui.locateOnScreen("placeyourbets.png", confidence=0.8)                       
                            if(len(str(sleepstrLockcheck))==44):
                                sleep_test=sleep_test+1
                                bet_count=bet_count+1
                                print(f' sleep bet count {bet_count}')
                                sleep(30)
                        except:
                            sleepstrLockcheck=''
                    
                    loop_count=0
                
            try: 
                #checking is connected or not
                pyautogui.click(textat_x,textat_y)
                try:
                    connection_check = pyautogui.locateOnScreen("Connnection.png", confidence=0.8)
                    # Check if the image was found and reload the page if it is
                    if connection_check is not None:
                        print(f'{str(connection_check)} length of this connection check: {len(str(connection_check))}')
                        pyautogui.hotkey('ctrl', 'r')   
                    else:
                        print("Image not found.")
                except Exception as e:
                    print(f"An error occurred: {e}")
                
                #checking place your bets lock
                lock_check = pyautogui.locateOnScreen("placeyourbets.png", confidence=0.8)
                
                pyautogui.click(textat_x,textat_y)
                sleep(1)
                # print(lock_check)
                if isFifth:
                    Bethistory=[]
                    pic = ImageGrab.grab(bbox=(499, 813, 706, 829))
                    pic.save("fifthtext.png")
                    isFifth=False
                    betted_on=''
                    sleep(1)
                    # last_char=extract_characters_from_image(image_path)
                    # add_to_fixed_length_array(Bethistory,last_char)
                    last_value_txt = get_text_at_position(textat_x,textat_y,moving_delay)
                    set_last_value(float(extract_numbers(last_value_txt)))
                    BestStrategy=extract_maxcount_from_image("ZeroLoop.png")
                    print(f'best strategy picked from loop {BestStrategy}')
                    
                strLockcheck = str(lock_check)
                if(loop_count!=0):

                    if(startingvaluefinal>target_amt_final):
                        break
                    if(txt<(startingvaluefinal+100)):
                        if(loss_count>=6):
                            loss_count=1

                # print(len(strLockcheck))                   
            except:
                strLockcheck=''
            
            if(len(strLockcheck)==44) :
 
                bet_count=bet_count+1
                
                if (bet_count % 5 == 0) and (not all_equal(Bethistory)):
                    sleep(25)
                    isFifth=True  
                    current_txt = get_text_at_position(textat_x,textat_y,moving_delay)
                    current_value_final=float(extract_numbers(current_txt))
                    if(last_value>current_value_final):
                        # print('inside true loop')
                        win_count=0
                        loss_count=loss_count+1
                        if(betted_on=='A'):
                            add_to_fixed_length_array(Bethistory,'B')
                        if(betted_on=='B'):
                            add_to_fixed_length_array(Bethistory,'A') 
                        
                        if loss_count==0:
                            repeat_count=fibo_series[loss_count]
                        elif loss_count==1:
                            repeat_count=fibo_series[loss_count]
                        elif loss_count==2: 
                            repeat_count=fibo_series[loss_count]
                        elif loss_count==3:
                            repeat_count=fibo_series[loss_count]
                        elif loss_count==4:
                            repeat_count=fibo_series[loss_count]
                        elif loss_count==5:
                            repeat_count=fibo_series[loss_count]
                        elif loss_count==6:
                            repeat_count=fibo_series[loss_count]
                        elif loss_count==7:
                            repeat_count=fibo_series[loss_count]
                        elif loss_count==8:
                            repeat_count=fibo_series[loss_count]
                        elif loss_count==9:
                            repeat_count=fibo_series[loss_count]
                        elif loss_count==10:
                            repeat_count=fibo_series[loss_count]
                        elif loss_count==11:
                            repeat_count=fibo_series[loss_count]
                        elif loss_count==12:
                            repeat_count=fibo_series[loss_count]
                        else:
                            repeat_count=loss_count*2   
                    # checks if its a tie                    
                    elif(last_value==current_value_final):


                        # add_to_fixed_length_array(Bethistory,'T')
                        loss_count=loss_count
                        repeat_count=repeat_count
                        win_count=win_count
                        
                    else:


                        if(betted_on=='A'):
                            add_to_fixed_length_array(Bethistory,'A')
                        if(betted_on=='B'):
                            add_to_fixed_length_array(Bethistory,'B')
                        
                        if(loss_count-2>=0):
                            loss_count=loss_count-2
                            repeat_count=fibo_series[loss_count]  
                        else:
                            loss_count=0
                            repeat_count=fibo_series[0]
                    win_count=win_count+1
                    betted_on=''

                else:

                    current_txt = get_text_at_position(textat_x,textat_y,moving_delay)
                    current_value_final=float(extract_numbers(current_txt))
                    if(loop_count!=0):
                        try:
                            if(last_value>current_value_final):
                                # print('inside true loop')
                                win_count=0
                                loss_count=loss_count+1
                                if(betted_on=='A'):
                                    add_to_fixed_length_array(Bethistory,'B')
                                if(betted_on=='B'):
                                    add_to_fixed_length_array(Bethistory,'A') 
                                
                                if loss_count==0:
                                    repeat_count=fibo_series[loss_count]
                                elif loss_count==1:
                                    repeat_count=fibo_series[loss_count]
                                elif loss_count==2: 
                                    repeat_count=fibo_series[loss_count]
                                elif loss_count==3:
                                    repeat_count=fibo_series[loss_count]
                                elif loss_count==4:
                                    repeat_count=fibo_series[loss_count]
                                elif loss_count==5:
                                    repeat_count=fibo_series[loss_count]
                                elif loss_count==6:
                                    repeat_count=fibo_series[loss_count]
                                elif loss_count==7:
                                    repeat_count=fibo_series[loss_count]
                                elif loss_count==8:
                                    repeat_count=fibo_series[loss_count]
                                elif loss_count==9:
                                    repeat_count=fibo_series[loss_count]
                                elif loss_count==10:
                                    repeat_count=fibo_series[loss_count]
                                elif loss_count==11:
                                    repeat_count=fibo_series[loss_count]
                                elif loss_count==12:
                                    repeat_count=fibo_series[loss_count]
                                else:
                                    repeat_count=loss_count*2   
                            # checks if its a tie                    
                            elif(last_value==current_value_final):
                                
                                loss_count=loss_count
                                repeat_count=repeat_count
                                win_count=win_count
                            else:
                                if(betted_on=='A'):
                                    add_to_fixed_length_array(Bethistory,'A')
                                if(betted_on=='B'):
                                    add_to_fixed_length_array(Bethistory,'B')
                                
                                if(loss_count-2>=0):
                                    loss_count=loss_count-2
                                    repeat_count=fibo_series[loss_count]
                                else:
                                    loss_count=0
                                    repeat_count=fibo_series[0]
                            
                                win_count=win_count+1
                        except Exception as e:
                            logging.error(f"An error occurred during the betting process: {e}", exc_info=True) 
                    try:
                        if loss_count>=6:
                            pic = pyautogui.screenshot()
                            pic.save("screenshot_"+str(loss_count)+".png")
                        if(loop_count==0):
                                pic = ImageGrab.grab(bbox=(564, 758, 709, 773))
                                pic.save("ZeroLoop.png")
                                sleep(1)
                                Bethistory=[]
                                # last_char=extract_characters_from_image("ZeroLoop.png")
                                # add_to_fixed_length_array(Bethistory,last_char)
                                BestStrategy=extract_maxcount_from_image("ZeroLoop.png")
                                print(f'best strategy picked from loop_count==0  {BestStrategy}')
                        else:
                            if(len(Bethistory)>=1):
                                if(BestStrategy=='B' and Bethistory[0]=='A'):
                                    BestStrategy='A'
                                elif(BestStrategy=='A' and Bethistory[0]=='B'):
                                    BestStrategy='B'
                            else:
                                pic = ImageGrab.grab(bbox=(564, 758, 709, 773))
                                pic.save("ZeroLoop.png")
                                sleep(1)
                                Bethistory=[]
                                BestStrategy=extract_maxcount_from_image("ZeroLoop.png")
                                print(f'best strategy picked from loop_count==0  {BestStrategy}')
                                
                    

                        
                        if (all_equal(Bethistory)):
                            if(Bethistory[0]=='A'):
                                betonA(repeat_count)
                            else:
                                betonB(repeat_count)
                            if(function_change<4):
                                function_change=function_change+1
                            else:
                                function_change=1
                            # pyautogui.click(textat_x,textat_y)
                            sleep(1)                  
                            last_value_txt = get_text_at_position(textat_x,textat_y,moving_delay)
                            set_last_value(float(extract_numbers(last_value_txt)))
                        else:
                            if(BestStrategy=='B'):
                                if function_change==1:  # Call function_one() twice for every even iteration

                                    if win_count>=4:
                                        betonA(repeat_count)
                                    else:
                                        betonB(repeat_count)                                    
    
                                    function_change=2
                                    # pyautogui.click(textat_x,textat_y)
                                    sleep(1)                  
                                    last_value_txt = get_text_at_position(textat_x,textat_y,moving_delay)
                                    set_last_value(float(extract_numbers(last_value_txt)))
                                    
                                elif function_change==2:  # Call function_one() twice for every even iteration

                                    if win_count>=4:
                                        betonA(repeat_count)
                                    else:
                                        betonB(repeat_count)  
                                    function_change=3
                                    sleep(1)                  
                                    last_value_txt = get_text_at_position(textat_x,textat_y,moving_delay)
                                    set_last_value(float(extract_numbers(last_value_txt)))
                                elif function_change==3:  # Call function_one() twice for every even iteration
                                    if(len(Bethistory)>=2):
                                        lenBet=len(Bethistory)
                                        if(Bethistory[lenBet-2]=='A'and Bethistory[lenBet-1]=='A'):
                                            betonB(repeat_count)     
                                        else:
                                            if win_count>=4:
                                                betonB(repeat_count)
                                            else:
                                                betonA(repeat_count)

                                    function_change=4
                                    sleep(1)                  
                                    last_value_txt = get_text_at_position(textat_x,textat_y,moving_delay)
                                    set_last_value(float(extract_numbers(last_value_txt)))
                                elif function_change==4:  # Call function_one() twice for every even iteration
                                    if(len(Bethistory)>=3):
                                        lenBet=len(Bethistory)
                                        if(Bethistory[lenBet-3]=='A' and Bethistory[lenBet-2]=='A'and Bethistory[lenBet-1]=='B'):
                                            betonB(repeat_count)     
                                        else:
                                            if win_count>=4:
                                                betonB(repeat_count)
                                            else:
                                                betonA(repeat_count)

                                    function_change=1
                                    # pyautogui.click(textat_x,textat_y)
                                    sleep(1)                  
                                    last_value_txt = get_text_at_position(textat_x,textat_y,moving_delay)
                                    set_last_value(float(extract_numbers(last_value_txt)))
                            else:
                                if function_change==1:  # Call function_one() twice for every even iteration

                                    if win_count>=4:
                                        betonB(repeat_count)
                                    else:
                                        betonA(repeat_count)                                    
    
                                    function_change=2
                                    # pyautogui.click(textat_x,textat_y)
                                    sleep(1)                  
                                    last_value_txt = get_text_at_position(textat_x,textat_y,moving_delay)
                                    set_last_value(float(extract_numbers(last_value_txt)))
                                    
                                elif function_change==2:  # Call function_one() twice for every even iteration
                                    
                                    if win_count>=4:
                                        betonB(repeat_count)
                                    else:
                                        betonA(repeat_count)  
                                    function_change=3

                                    sleep(1)                  
                                    last_value_txt = get_text_at_position(textat_x,textat_y,moving_delay)
                                    set_last_value(float(extract_numbers(last_value_txt)))
                                elif function_change==3:  # Call function_one() twice for every even iteration

                                    if(len(Bethistory)>=2):
                                        # lenBet=len(Bethistory)
                                        # if(Bethistory[lenBet-2]=='A'and Bethistory[lenBet-1]=='A'):
                                        #     betonB(repeat_count)     
                                        # else:
                                        if win_count>=4:
                                            betonA(repeat_count)
                                        else:
                                            betonB(repeat_count)
                                    function_change=4
                                    # pyautogui.click(textat_x,textat_y)
                                    sleep(1)                  
                                    last_value_txt = get_text_at_position(textat_x,textat_y,moving_delay)
                                    set_last_value(float(extract_numbers(last_value_txt)))
                                elif function_change==4:  # Call function_one() twice for every even iteration

                                    # Preventing AABB pattern
                                    if(len(Bethistory)>=3):
                                        if win_count>=4:
                                            betonA(repeat_count)
                                        else:
                                            betonB(repeat_count)
                                    function_change=1
                                    sleep(1)                  
                                    last_value_txt = get_text_at_position(textat_x,textat_y,moving_delay)
                                    set_last_value(float(extract_numbers(last_value_txt)))

                        loop_count=loop_count+1
                        startingvaluefinal=last_value
                        

                        print(f'Checking Bet history {Bethistory}')
                        logging.info(f'Checking Bet history {Bethistory}')
                        
                        # print(Bethistory)
                        print(f'Loss_count {loss_count}')
                        print(f'betcount  {bet_count}')
                        sleep(23)

                    except Exception as e:
                        logging.error(f"An error occurred during the betting process: {e}", exc_info=True)
                        break
            else:
                strLockcheck=''
        else:
            # bet_analyzer.analyze_and_push()
            # pyautogui.alert('Target Achieved')
            play_alarm() 
            # close_chrome_tabs()
            sleep(10)
            # shutdown_system()
            logging.info("Condition not met, alarm beeped.")
            break
            # sleep(10)  # Wait before rechecking
except Exception as e:
    logging.error(f"An error occurred in the main function: {e}", exc_info=True)
    print(f"An error occurred: {e}. Please go to the original screen.")
    pyautogui.alert(f"An error occurred: {e}. Please go to the original screen.")


