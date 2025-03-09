import webbrowser
import pyautogui
import time
import threading
import commands as com
import re

# Open the website
def open_website(domain):
    domain = domain.lower().replace(" ", "")
    url = f'https://www.{domain}'
    webbrowser.open(url)
    return True

# Scroll the page continuously
def scroll_mouse(amount, duration=20):
    def continuous_scroll():
        start_time = time.time()
        while scrolling and (time.time() - start_time < duration):
            pyautogui.scroll(-amount)  # Reverse the scrolling direction
            time.sleep(1)  # Make the scrolling even slower
        stop_scrolling()

    global scrolling
    scrolling = True
    scroll_thread = threading.Thread(target=continuous_scroll)
    scroll_thread.start()
    return True

# Stop scrolling
def stop_scrolling():
    global scrolling
    scrolling = False
    return True

def move_mouse(x, y):
    pyautogui.moveTo(x, y)
    return True

def click():
    pyautogui.click()
    return True

def double_click():
    pyautogui.doubleClick()
    return True

def write(text):
    pyautogui.write(text)
    return True

def wait(seconds):
    time.sleep(seconds)
    return True

def execute_command(command):
    command_name, *params = command.split('(')
    params = params[0][:-1].split(',') if params else []
    params = [param.strip().strip(')') for param in params]
    
    if command_name == "move_mouse":
        move_mouse(int(params[0]), int(params[1]))
    elif command_name == "click":
        click()
    elif command_name == "double_click":
        double_click()
    elif command_name == "scroll_mouse":
        scroll_mouse(int(params[0]))
    elif command_name == "open_website":
        open_website(params[0])
    elif command_name == "write":
        write(params[0])
    elif command_name == "wait":
        wait(int(params[0]))
    else:
        print(f"Unknown command: {command}")