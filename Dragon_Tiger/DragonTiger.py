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
import numpy as np
from  GetBalance import get_balance
import os

# Define a global variable to store the content of the cookie
cookie_content = None

# Function to read the cookie content from the file
def load_cookie(file_path='DragonHeaders.txt'):
    global cookie_content
    if cookie_content is None:
        with open(file_path, 'r') as file:
            cookie_content = file.read()
    return cookie_content

def is_alternating(arr):
    # Check if the length of the array is less than 4
    if len(arr) < 4:
        return False
    
    # Get the last 4 characters of the array
    last_four = arr[-4:]
    
    # Check if the last four characters alternate
    if (last_four[0] != last_four[1] and
        last_four[1] != last_four[2] and
        last_four[2] != last_four[3] and
        last_four[0] == last_four[2] and
        last_four[1] == last_four[3]):
        return True
    elif(last_four[-1]=='I'):
        return True
    return False



def set_First_target(value):
    global First_target
    First_target = value


def set_gtarget_breaking(value):
    global gtarget_breaking
    gtarget_breaking=value

def set_gtarget_amt(value):
    global gtarget_amt
    gtarget_amt=value


set_First_target(0)

def set_last_value(value):
    global last_value
    last_value = value

def set_new_target_val(value):
    global new_target
    new_target = value

def set_last_value_at(value):
    global at_last_value
    at_last_value = value

def set_betted_on(value):
    global betted_on
    betted_on = value

def main():
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

    relative_Ax = 771 / 1920  # Relative position on X-axis
    relative_Ay = 770 / 1080   # Relative position on Y-axis
    A_x = screenWidth*relative_Ax
    A_y = screenHeight*relative_Ay

    # radius is common for moving cursor in round--------------
    # ---------------------------------------------------------
    moving_r = 10
    # ----------------------------------------------------------


    # B--axis for BetOnB---------------------------------------
    # 1050, 800, 20-for Santosh Bhaiya Machine-----------------

    relative_Bx = 1082 / 1920  # Relative position on X-axis
    relative_By = 765 / 1080   # Relative position on Y-axis

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
    last_value=None
    loss_count=0
    win_count=0
    loop_count=0
    repeat_count=1
    bet_count=0
    startingvaluefinal=0

    # Define the global variable
    

    def set_betted_on(value):
        global betted_on
        betted_on = value

    def compare_betted_on(value):
        global betted_on
        if betted_on == value:
            return True
        else:
            return False

    # for first time
    set_betted_on(None)

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


    def get_last_dragon():
        # Load the image
        try:
            image_path = 'DragonRoar.png'
            image = Image.open(image_path)

            # Convert the image to a NumPy array
            image_array = np.array(image)

            # Define color thresholds for red, blue, and green
            blue_threshold = ([0, 0, 100], [50, 50, 255])  # Approximate blue range
            red_threshold = ([100, 0, 0], [255, 50, 50])   # Approximate red range
            green_threshold = ([0, 100, 0], [50, 255, 50]) # Approximate green range

            # Function to check if a pixel falls within the given color range
            def is_color(pixel, color_range):
                lower, upper = color_range
                return all(lower[i] <= pixel[i] <= upper[i] for i in range(3))

            # Extract the middle row for color detection
            height, width, _ = image_array.shape
            middle_row = image_array[height // 2]

            # Detect the positions of circles by identifying color changes
            circle_positions = []
            current_color = None

            for x in range(width):
                pixel = middle_row[x, :3]  # Get RGB values of the pixel

                if is_color(pixel, blue_threshold):
                    new_color = 'T'
                elif is_color(pixel, red_threshold):
                    new_color = 'D'
                elif is_color(pixel, green_threshold):
                    new_color = 'I'
                else:
                    new_color = None

                # If a new color is detected, it marks the start of a new circle
                if new_color and new_color != current_color:
                    circle_positions.append(x)
                    current_color = new_color

            # Calculate the average distance between circles to determine sample_step
            if len(circle_positions) > 1:
                sample_step = int(np.mean(np.diff(circle_positions)))
            else:
                sample_step = width // len(circle_positions)
      

            # Iterate over detected positions to extract the sequence
            sequence = ""
            for x in circle_positions:
                pixel = middle_row[x, :3]  # Get RGB values of the pixel

                if is_color(pixel, blue_threshold):
                    sequence += 'T'
                elif is_color(pixel, red_threshold):
                    sequence += 'D'
                elif is_color(pixel, green_threshold):
                    sequence += 'I'

            return sequence
        except:
            return 'T'


    def extract_characters_from_image(image_path):
        # Load the image
        img = Image.open(image_path)

        # Convert image to RGB and extract pixels
    
        # Fallback to OCR if no colors were detected
        text = pytesseract.image_to_string(img, config='--psm 6')
        print(txt)
        filtered_text = ''.join(c for c in text if c in 'DT')
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



    # Get the current working directory
    current_dir = os.getcwd()
    log_dir = os.path.join(current_dir+'\Dragon_Tiger', 'dragonglogs')

    # Create the directory if it doesn't exist
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
            brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
        elif platform.system() == "Darwin":  # macOS
            brave_path = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
        elif platform.system() == "Linux":
            brave_path = "/usr/bin/brave"
        else:
            raise OSError("Unsupported operating system")

        # Prepare the command for launching Chrome in incognito mode
        command = [brave_path, '--incognito', url]

        # Launch Chrome in incognito mode with the specified URL
        try:
            subprocess.run(command, check=True)
        except FileNotFoundError:
            print(f"Error: Chrome executable not found at {brave_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error running command: {e}")




    def move_cursor_in_random_circles(center_x, center_y, radius, duration=3):
        """Move the cursor in random circles around the given center point for the specified duration with human-like imperfections.
        Returns the final x and y coordinates of the cursor."""
        
        screen_width, screen_height = pyautogui.size()  # Get screen dimensions
        start_time = time.time()
        
        # Initialize final position variables
        final_x = center_x
        final_y = center_y
        
        while time.time() - start_time < duration:
            num_steps = random.randint(5, 10)  # More steps for smoother circles
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


    def betonD(no_click):
        # pyautogui.click(x=600,y= 600,clicks=no_click)
        # final_x, final_y =move_cursor_in_random_circles(A_x, A_y, moving_r)  # Move cursor in random circles around the betting point
        # sleep(1)  # Short delay to mimic human behavior
        pyautogui.click(x=A_x, y=A_y,clicks=no_click*2)
        set_betted_on('D')
        # logging.info("Betting on A --Current value:{starting_value_final} Target Value:{target_amt}  Loss Count: {loss_count} Win Count:{win_count} Repeat_count:{repeat_count}")
        logging.info(f"D,{startingvaluefinal},{target_amt},{loss_count},{win_count}")
        write_to_csv(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'A', startingvaluefinal, target_amt, loss_count, win_count)
        sleep(3)



    def betonT(no_click):
        # pyautogui.click(x=740,y= 600,clicks=no_click)
        """Perform betting action on B."""
        # final_x, final_y =move_cursor_in_random_circles(B_x,B_y,moving_r)  # Move cursor in random circles around the betting point
        # sleep(1)  # Short delay to mimic human behavior
        pyautogui.click(x=B_x,y=B_y,clicks=no_click*2)

        set_betted_on('T')
        # logging.info("Betting on B --Loss Count: {loss_count} Win Count:{win_count} Repeat_count:{repeat_count}")
        logging.info(f"T,{startingvaluefinal},{target_amt},{loss_count},{win_count}")
        write_to_csv(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'B', startingvaluefinal, target_amt, loss_count, win_count)
        sleep(3)



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

    if(First_target==0):
        thread = threading.Thread(target=open_incognito_website(url=BaseUrl))
        thread.start()
        thread.join()

        target_amt=pyautogui.prompt(text="",title="Enter your target")
        set_gtarget_amt(target_amt)
        sleep(2)

        target_breaking=pyautogui.prompt(text="",title="Enter your target break")
        set_gtarget_breaking(target_breaking)
        sleep(1)
    else:
        target_amt=gtarget_amt
        target_breaking=gtarget_breaking

    Target_break=float(target_breaking)




    def set_last_value(value):
        global last_value
        last_value = value

    def set_new_target_val(value):
        global new_target
        new_target = value


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
        
        sleep(1)
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
        if len(arr) > 8:
            arr.pop(0)  # Remove the oldest element
        return arr

    # To check values are equal
    def all_equal(arr):
        # Check if the length of the array is less than 4
        if len(arr) < 4:
            return False
        # Check if all elements are equal
        return all(x == arr[0] for x in arr)



    # 
    sleep(2)

    starting_value =get_balance()
    print(starting_value)
    txt = starting_value
    flag=False
    targetyes=0

    try:    
        # pyautogui.click(x=607, y=640)                                                               
        startingvaluefinal=float(txt)
        Target_break_final=float(Target_break)
        set_new_target_val(startingvaluefinal+Target_break_final)
        target_amt_final=float(target_amt)
        logging.info(f"Starting value: {startingvaluefinal}")
        logging.info(f"Target amount: {target_amt}")
        logging.info("Betted On,CurrentValue,TargetAmt,Losscount,Wincount")
        while True:             
            while startingvaluefinal<target_amt_final:
                if(loop_count!=0):
                    current_txt = get_balance()
                    startingvaluefinal=current_txt
                try:  
                    try:
                        connection_check = pyautogui.locateOnScreen("Connnection.png", confidence=0.8)
                        # Check if the image was found and reload the page if it is
                        if connection_check is not None:
                            # print(f'{str(connection_check)} length of this connection check: {len(str(connection_check))}')
                            pyautogui.click(1419, 263) 
                            sleep(5)
                    except:
                        exc=''
                    lock_check = pyautogui.locateOnScreen("Dragon_Tiger\placeyourbets.png", confidence=0.8)
                    
                    sleep(1)
                    # print(lock_check)
                    strLockcheck = str(lock_check)
                    if(loop_count!=0):

                        if(startingvaluefinal>new_target):
                            # set_First_target(1)
                            set_First_target(1)
                            user_response=pyautogui.confirm(f' Money is A Dirty thing. \n Mini Target Acheieved 😊 \n Please withdraw money and dont let it go!\n Disclaimer: \n Always do this on starting of 5 line. \n Please use phone to withdraw. \n Press Ok to Play again.')       
                            # Check the response and act accordingly
                            print(f'New Target Achieved {new_target}')
                            set_new_target_val(startingvaluefinal+Target_break_final)
                            #reset values
                            Bethistory=[]
                            loss_count=0
                            win_count=0
                            repeat_count=1
                            if user_response == 'OK':
                                main()
                            else:
                                break
                            # print(f'New Target Achieved {new_target}')
                            
                        if(txt<(startingvaluefinal+100)):
                            if(loss_count>=6):
                                loss_count=1

                    # print(len(strLockcheck))                   
                except:
                    strLockcheck=''
                
                if(len(strLockcheck)==44) :
    
                    bet_count=bet_count+1
                    sleep(2)
                    current_txt = get_balance()
                    current_value_final=current_txt
                    if(loop_count!=0):
                        try:
                            base_amt=9
                            if(last_value>current_value_final):
                                # print('inside true loop')
                                Tie_value=(base_amt*(repeat_count*2))/2
                                if((last_value-Tie_value)==current_value_final):
                                    # its a tie
                                    add_to_fixed_length_array(Bethistory,'I')
                                elif(betted_on=='D'):
                                    add_to_fixed_length_array(Bethistory,'T')
                                elif(betted_on=='T'):
                                    add_to_fixed_length_array(Bethistory,'D') 

                                win_count=0
                                loss_count=loss_count+1
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
                                # add_to_fixed_length_array(Bethistory,'I')
                                loss_count=loss_count
                                repeat_count=repeat_count
                                win_count=win_count
                            else:
                                if(betted_on=='D'):
                                    add_to_fixed_length_array(Bethistory,'D')
                                if(betted_on=='T'):
                                    add_to_fixed_length_array(Bethistory,'T')                                                                                               
                                
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
                        if(is_alternating(Bethistory)):
                            #skipping this bet
                            # next_multiple_of_5 = (bet_count + random.randint(5,6)) // 5 * 5
                            # noMultiple=next_multiple_of_5-3
                            # loop_condition=noMultiple-bet_count
                            loop_condition=random.randint(5,6)
                            sleep_test=0
                            while(sleep_test<loop_condition):
                                try:
                                    connection_check = pyautogui.locateOnScreen("Connnection.png", confidence=0.8)
                                    # Check if the image was found and reload the page if it is
                                    if connection_check is not None:
                                        # print(f'{str(connection_check)} length of this connection check: {len(str(connection_check))}')
                                        pyautogui.click(1419, 263) 
                                        sleep(5)
                                except:
                                    exc=''
                                    # print('Unable to locate connection')                    
                                try:
                                    sleepstrLockcheck = pyautogui.locateOnScreen("placeyourbets.png", confidence=0.8)                       
                                    if(len(str(sleepstrLockcheck))==44):
                                        sleep_test=sleep_test+1
                                        bet_count=bet_count+1
                                        print(f'sleep bet count {bet_count}')
                                        sleep(15)
                                except:
                                    sleepstrLockcheck=''
                            Bethistory=[]
                            loop_count=0
                            #reset values
                            Bethistory=[]
                            win_count=0
                            repeat_count=fibo_series[loss_count]
                        

                        else:
                            if loss_count>=6:
                                pic = pyautogui.screenshot()
                                pic.save("screenshot_"+str(loss_count)+".png")
                            
                            if(loop_count==0):
                                pic = ImageGrab.grab(bbox=(447, 733, 703, 753))
                                pic.save("DragonRoar.png")
                                sleep(1)
                                lastWinner=get_last_dragon()
                                if(lastWinner=='D'):
                                    betonD(repeat_count) 
                                elif(lastWinner=='T'):
                                    betonT(repeat_count)
                                else:
                                    even_number= random.randint(1, 10) 
                                    if(even_number%2==0):
                                        betonD(repeat_count)
                                    else:
                                        betonT(repeat_count)

                                
                            if(len(Bethistory)>=1):
                                if(Bethistory[len(Bethistory)-1]=='I'):
                                    if(Bethistory[len(Bethistory)-2]=='D'):
                                        betonD(repeat_count)
                                    else:
                                        betonT(repeat_count)

                                if(Bethistory[len(Bethistory)-1]=='D'):
                                    betonD(repeat_count)
                                elif(Bethistory[len(Bethistory)-1]=='T'):
                                    betonT(repeat_count)

                            loop_count=loop_count+1
                        
                                                
                        last_value = get_balance()
                        startingvaluefinal=last_value
                        set_last_value(last_value)


                        

                        print(f'Checking Bet history {Bethistory}')
                        logging.info(f'Checking Bet history {Bethistory}')
                        
                        print(Bethistory)
                        print(f'Loss_count {loss_count}')
                        print(f'betcount  {bet_count}')

                        sleep(10)

                    except Exception as e:
                        logging.error(f"An error occurred during the betting process: {e}", exc_info=True)
                        break
                else:
                    strLockcheck=''
            else:
                # bet_analyzer.analyze_and_push()
                shutdown_system()
                # pyautogui.alert('Target Achieved')
                play_alarm() 
                # close_chrome_tabs()
                sleep(10)
                logging.info("Condition not met, alarm beeped.")
                break
                # sleep(10)  # Wait before rechecking
    except Exception as e:
        logging.error(f"An error occurred in the main function: {e}", exc_info=True)
        print(f"An error occurred: {e}. Please go to the original screen.")
        pyautogui.alert(f"An error occurred: {e}. Please go to the original screen.")

if __name__ == "__main__":
    main()


