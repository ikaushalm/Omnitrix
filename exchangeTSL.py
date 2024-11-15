import base64
import bet_analyzer
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

# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------
# --------------Configuration Files------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------


# A--axis for BetOnA---------------------------------------
# 850, 800, 20 -for Santosh Bhaiya Machine-----------------
A_x = 850
A_y = 800

# radius is common for moving cursor in round--------------
# ---------------------------------------------------------
moving_r = 20 
# ----------------------------------------------------------


# B--axis for BetOnB---------------------------------------
# 1050, 800, 20-for Santosh Bhaiya Machine-----------------
B_x = 1050
B_y = 800

# ---------------------------------------------------------
# get_text_at_position
# 1150,135,0.5 -for Santosh Bhaiya Machine-----------------
textat_x=1150
textat_y=135
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


function_one=1
function_change=1
last_value=None
loss_count=0
win_count=0
loop_count=0
repeat_count=1
bet_count=0
startingvaluefinal=0


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
    sleep(1)  # Short delay to mimic human behavior
    pyautogui.click(x=final_x, y=final_y,clicks=no_click)
    # logging.info("Betting on A --Current value:{starting_value_final} Target Value:{target_amt}  Loss Count: {loss_count} Win Count:{win_count} Repeat_count:{repeat_count}")
    logging.info(f"A,{startingvaluefinal},{target_amt},{loss_count},{win_count}")
    write_to_csv(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'A', startingvaluefinal, target_amt, loss_count, win_count)



def betonB(no_click):
    # pyautogui.click(x=740,y= 600,clicks=no_click)
    """Perform betting action on B."""
    final_x, final_y =move_cursor_in_random_circles(B_x,B_y,moving_r)  # Move cursor in random circles around the betting point
    sleep(1)  # Short delay to mimic human behavior
    pyautogui.click(x=final_x,y=final_y,clicks=no_click)
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

#to take screen out of this ide
target_amt=pyautogui.prompt(text="",title="Enter your target")
sleep(2)



def set_last_value(value):
    global last_value
    last_value = value


def set_last_value_at(value):
    global at_last_value
    at_last_value = value

def get_text_at_position(x, y, duration=0.5):
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


starting_value = get_text_at_position(textat_x,textat_y,moving_delay)
txt = extract_numbers(starting_value)
flag=False
targetyes=0

try:    
    # pyautogui.click(x=607, y=640)                                                               
    startingvaluefinal=float(txt)
    function_change=1
    target_amt_final=float(target_amt)
    logging.info(f"Starting value: {startingvaluefinal}")
    logging.info(f"Target amount: {target_amt}")
    logging.info("Betted On,CurrentValue,TargetAmt,Losscount,Wincount")
    while True:     
        while last_value<target_amt_final:
            try:               
                lock_check = pyautogui.locateOnScreen("placeyourbets.png", confidence=0.8)
                pyautogui.click(textat_x,textat_y)
                sleep(1)
                # print(lock_check)
                bet_count=bet_count+1
                strLockcheck = str(lock_check)
                # print(len(strLockcheck))
                if(loop_count!=0):
                    current_txt = get_text_at_position(textat_x,textat_y,moving_delay)
                    startingvaluefinal=float(extract_numbers(current_txt))
                    if(startingvaluefinal>target_amt_final):
                        break

                
            except:
                strLockcheck=''
            if(len(strLockcheck)==44) :
                current_txt = get_text_at_position(textat_x,textat_y,moving_delay)
                current_value_final=float(extract_numbers(current_txt))
                if(loop_count!=0):
                    # print(last_value)
                    # print(current_value_final)
                    if(last_value>current_value_final):
                        # print('inside true loop')
                        win_count=0
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
                    # checks if its a tie                    
                    elif(last_value==current_value_final):
                        loss_count=loss_count
                        repeat_count=repeat_count
                        win_count=win_count
                    else:
                        repeat_count=1
                        loss_count=0
                        win_count=win_count+1
                try:
                    if loss_count>=6:
                        pic = pyautogui.screenshot()
                        pic.save("screenshot_"+str(loss_count)+".png")
                                            

                    if function_change==1:  # Call function_one() twice for every even iteration
                        
                        # if bet_count%3==0:
                        #     betonA(repeat_count)
                        # else:
                        if win_count>=2:
                            betonA(repeat_count)
                        else:
                            if loss_count<=2:
                                betonB(repeat_count)
                            else:
                                betonA(repeat_count)

                        function_change=2
                        pyautogui.click(textat_x,textat_y)
                        sleep(1)                  
                        last_value_txt = get_text_at_position(textat_x,textat_y,moving_delay)
                        set_last_value(float(extract_numbers(last_value_txt)))
                        
                    elif function_change==2:  # Call function_one() twice for every even iteration
                        # if bet_count%3==0:
                        #     betonA(repeat_count)
                        # else:                        
                        if win_count>=2:
                            betonA(repeat_count)
                        else:
                            if loss_count<=2:
                                betonB(repeat_count)
                            else:
                                betonA(repeat_count)
                        function_change=3
                        pyautogui.click(textat_x,textat_y)
                        sleep(1)                  
                        last_value_txt = get_text_at_position(textat_x,textat_y,moving_delay)
                        set_last_value(float(extract_numbers(last_value_txt)))
                    elif function_change==3:  # Call function_one() twice for every even iteration
                        # if bet_count%3==0:
                        #     betonA(repeat_count)
                        # else: 
                        if win_count>=2:
                            betonB(repeat_count)
                        else:
                            if loss_count<=2:
                                betonA(repeat_count)
                            else:
                                betonB(repeat_count)
                        function_change=4
                        pyautogui.click(textat_x,textat_y)
                        sleep(1)                  
                        last_value_txt = get_text_at_position(textat_x,textat_y,moving_delay)
                        set_last_value(float(extract_numbers(last_value_txt)))
                    elif function_change==4:  # Call function_one() twice for every even iteration
                        # if bet_count%3==0:
                        #     betonA(repeat_count)
                        # else:  
                        if win_count>=2:
                            betonB(repeat_count)
                        else:
                            if loss_count<=2:
                                betonA(repeat_count)
                            else:
                                betonB(repeat_count)
                        function_change=1
                        pyautogui.click(textat_x,textat_y)
                        sleep(1)                  
                        last_value_txt = get_text_at_position(textat_x,textat_y,moving_delay)
                        set_last_value(float(extract_numbers(last_value_txt)))
                    loop_count=loop_count+1
                    sleep(15)    
                except Exception as e:
                    logging.error(f"An error occurred during the betting process: {e}", exc_info=True)
                    break
            else:
                strLockcheck=''
        else:
            bet_analyzer.analyze_and_push()
            play_alarm() 
            close_chrome_tabs()
            sleep(10)
            shutdown_system()
            logging.info("Condition not met, alarm beeped.")
            break
            # sleep(10)  # Wait before rechecking
except Exception as e:
    logging.error(f"An error occurred in the main function: {e}", exc_info=True)
    print(f"An error occurred: {e}. Please go to the original screen.")



