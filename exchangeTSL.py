import math
import random
import subprocess
import sys
import bet_analyzer


def install(package):
    """Install the package using pip."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install_dependencies():
    """Check and install missing dependencies."""
    dependencies = [
        'pyautogui',
        'pytesseract',
        'Pillow',
        'setuptools'
    ]
    
    # Try importing pkg_resources to check if setuptools is installed
    try:
        import pkg_resources
    except ImportError:
        print("pkg_resources not found. Installing setuptools...")
        install('setuptools')
    
    import pkg_resources
    
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    for package in dependencies:
        if package not in installed_packages:
            print(f"Installing {package}...")
            install(package)
        else:
            print(f"{package} is already installed.")

# Call the function to check and install dependencies
check_and_install_dependencies()

# Import other necessary modules after ensuring dependencies

from time import sleep
import pyautogui
import pytesseract
from PIL import ImageGrab
import re
import logging
import winsound
import os
from datetime import datetime
import time
import csv
import platform

# from twilio.rest import Client

# # Your Twilio Account SID and Auth Token
# account_sid = 'ACcf5c43d3ca76cbd9cc51b4b2ae1dff6c'
# auth_token = '6fa491c1275def4ac4d2dd608c6fef09'

# # Create a Twilio client
# client = Client(account_sid, auth_token)

# # Your Twilio phone number (obtained from Twilio)
# from_phone = '+14144859675'

# # The recipient's phone number
# to_phone = '+917786868782'




function_one=1
function_change=1
last_value=None
loss_count=0
win_count=0
loop_count=0
repeat_count=1
bet_count=0
startingvaluefinal=0


at_last_value=None
at_loss_count=0
at_loop_count=0
at_repeat_count=1
at_function_change=1


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


def move_cursor_in_random_circles(center_x, center_y, radius, duration=6):
    """Move the cursor in random circles around the given center point for the specified duration with human-like imperfections."""
    
    screen_width, screen_height = pyautogui.size()  # Get screen dimensions
    start_time = time.time()
    
    while time.time() - start_time < duration:
        num_steps = random.randint(10, 20)  # More steps for smoother circles
        for step in range(num_steps):
            angle = 2 * math.pi * step / num_steps
            
            # Introduce slight random deviations
            deviation_angle = random.uniform(-0.2, 0.2)
            x = center_x + (radius + random.uniform(-5, 5)) * math.cos(angle + deviation_angle)
            y = center_y + (radius + random.uniform(-5, 5)) * math.sin(angle + deviation_angle)
            
            # Ensure cursor stays within screen bounds
            x = max(0, min(screen_width - 1, x))
            y = max(0, min(screen_height - 1, y))
            
            # Move cursor with variable speed
            move_duration = random.uniform(0.1, 0.5)  # Slightly longer durations
            pyautogui.moveTo(x, y, duration=move_duration)
            
            # Add a variable delay for more natural movement
            time.sleep(random.uniform(0.05, 0.2))
        
        # Randomly adjust radius and center for the next circle
        radius = max(5, radius + random.uniform(-10, 10))  # Prevent radius from going too small
        center_x = max(0, min(screen_width - 1, center_x + random.uniform(-20, 20)))  # Adjust center with bounds check
        center_y = max(0, min(screen_height - 1, center_y + random.uniform(-20, 20)))  # Adjust center with bounds check

def betonA(no_click):
    # pyautogui.click(x=600,y= 600,clicks=no_click)
    move_cursor_in_random_circles(850, 800, 30)  # Move cursor in random circles around the betting point
    sleep(1)  # Short delay to mimic human behavior
    pyautogui.click(x=850, y=800,clicks=no_click)
    # logging.info("Betting on A --Current value:{starting_value_final} Target Value:{target_amt}  Loss Count: {loss_count} Win Count:{win_count} Repeat_count:{repeat_count}")
    logging.info(f"A,{startingvaluefinal},{target_amt},{loss_count},{win_count}")
    write_to_csv(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'A', startingvaluefinal, target_amt, loss_count, win_count)



def betonB(no_click):
    # pyautogui.click(x=740,y= 600,clicks=no_click)
    """Perform betting action on B."""
    move_cursor_in_random_circles(1050, 800, 30)  # Move cursor in random circles around the betting point
    sleep(1)  # Short delay to mimic human behavior
    pyautogui.click(x=1050,y= 800,clicks=no_click)
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

# get Teserect Executable Location
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#to take screen out of this ide
target_amt=pyautogui.prompt(text="",title="Enter your target")
sleep(2)


def set_last_value(value):
    global last_value
    last_value = value


def set_last_value_at(value):
    global at_last_value
    at_last_value = value

starting_value = ImageGrab.grab(bbox=(1109, 131, 1239, 152))
txt = extract_numbers(pytesseract.image_to_string(starting_value,config='--psm 6'))
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
        while startingvaluefinal<target_amt_final:
            try:               
                lock_check = pyautogui.locateOnScreen("placeyourbets.png", confidence=0.8)
                pyautogui.click(1150,135)
                sleep(1)
                # print(lock_check)
                bet_count=bet_count+1
                strLockcheck = str(lock_check)
                # print(len(strLockcheck))
                
            except:
                strLockcheck=''
            if(len(strLockcheck)==44) :
                sleep(2)
                current_value = ImageGrab.grab(bbox=(1109, 131, 1239, 152))
                current_txt = pytesseract.image_to_string(current_value,config='--psm 6')
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
                        pyautogui.click(1150,135)
                        sleep(2)
                        last_value_pic = ImageGrab.grab(bbox=(1109, 131, 1239, 152))
                        last_value_txt = pytesseract.image_to_string(last_value_pic,config='--psm 6')
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
                        pyautogui.click(1150,135)
                        sleep(2)                   
                        last_value_pic = ImageGrab.grab(bbox=(1109, 131, 1239, 152))
                        last_value_txt = pytesseract.image_to_string(last_value_pic,config='--psm 6')
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
                        pyautogui.click(1150,135)
                        sleep(2)
                        last_value_pic = ImageGrab.grab(bbox=(1109, 131, 1239, 152))
                        last_value_txt = pytesseract.image_to_string(last_value_pic,config='--psm 6')
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
                        pyautogui.click(1150,135)
                        sleep(2)
                        last_value_pic = ImageGrab.grab(bbox=(1109, 131, 1239, 152))
                        last_value_txt = pytesseract.image_to_string(last_value_pic,config='--psm 6')
                        set_last_value(float(extract_numbers(last_value_txt)))
                    loop_count=loop_count+1
                    starting_value = ImageGrab.grab(bbox=(1109, 131, 1239, 152))
                    txt = pytesseract.image_to_string(starting_value,config='--psm 6')
                    startingvaluefinal=float(extract_numbers(txt))
                    sleep(20)    
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
            # logging.info("Condition not met, alarm beeped.")
            # sleep(10)  # Wait before rechecking
except Exception as e:
    logging.error(f"An error occurred in the main function: {e}", exc_info=True)
    print(f"An error occurred: {e}. Please go to the original screen.")



