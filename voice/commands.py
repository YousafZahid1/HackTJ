import webbrowser
import pyautogui
import time

def move_mouse(x, y):
    pyautogui.moveTo(x, y)
    return True
    
def click_mouse():
    pyautogui.click()
    return True

def double_click_mouse():
    pyautogui.doubleClick()
    return True

def scroll_mouse(amount):
    pyautogui.scroll(amount)
    return True
# Make scroll mouse relative to page

def drag_mouse(x, y):
    pyautogui.dragTo(x, y)
    return True

def open_website(domain):
    domain = domain.lower().replace(" ", "")
    url = f'https://www.{domain}'
    
    webbrowser.open(url)
    return True

def find_button(button):
    # Make the search related to text
    button = button.lower().replace(" ", "")
    pyautogui.hotkey('ctrl', 'f')
    pyautogui.write(button)
    pyautogui.press('enter')
    return True

def navigate_to_section(section):
    section = section.lower().replace(" ", "")
    pyautogui.hotkey('ctrl', 'f')
    pyautogui.write(section)
    pyautogui.press('enter')
    return True

def write_text(text):
    pyautogui.write(text)
    return True
'''
def search_bar(text):
    pyautogui.hotkey('ctrl', 'l')
    pyautogui.write(text)
    pyautogui.press('enter')
    return True
    '''

def capture_region(x, y, width, height):
    region = (x, y, width, height)
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save("screenshot_region.png")
    return True

def wait(seconds):
    time.sleep(seconds)
    return True

def locate_and_click(image_path):
    time.sleep(1)  # Add a delay to ensure the screen is fully loaded
    location = pyautogui.locateOnScreen(image_path)
    if location:
        pyautogui.moveTo(location)
        pyautogui.click()
        return True
    else:
        print(f"Element not found: {image_path}")
        return False

def search_product(query):
    if locate_and_click('search_bar.png'):  # Image of the search bar
        pyautogui.write(query)
        pyautogui.press('enter')
        return True
    return False

def select_product(image_path):
    return locate_and_click(image_path)  # Image of the specific product

def add_to_cart():
    pyautogui.hotkey('ctrl', 'f')
    pyautogui.write('add to cart')
    pyautogui.press('enter')
    return True

def proceed_to_checkout():
    pyautogui.hotkey('ctrl', 'f')
    pyautogui.write('proceed to checkout')
    pyautogui.press('enter')
    return True

def fill_form_field(field, value):
    pyautogui.hotkey('ctrl', 'f')
    pyautogui.write(field)
    pyautogui.press('enter')
    pyautogui.write(value)
    return True

def submit_form():
    pyautogui.press('enter')
    return True

def execute_command(command):
    # Implement the logic to handle different commands
    command_name, *params = command.split('(')
    params = params[0][:-1].split(',') if params else []
    
    if command_name == "move_mouse":
        move_mouse(int(params[0]), int(params[1]))
    elif command_name == "click_mouse":
        click_mouse()
    elif command_name == "double_click_mouse":
        double_click_mouse()
    elif command_name == "scroll_mouse":
        scroll_mouse(int(params[0]))
    elif command_name == "drag_mouse":
        drag_mouse(int(params[0]), int(params[1]))
    elif command_name == "open_website":
        open_website(params[0])
    elif command_name == "find_button":
        find_button(params[0])
    elif command_name == "navigate_to_section":
        navigate_to_section(params[0])
    elif command_name == "write_text":
        write_text(params[0])
    elif command_name == "capture_region":
        capture_region(int(params[0]), int(params[1]), int(params[2]), int(params[3]))
    elif command_name == "wait":
        wait(int(params[0]))
    elif command_name == "search_product":
        search_product(params[0])
    elif command_name == "select_product":
        select_product(params[0])
    elif command_name == "add_to_cart":
        add_to_cart()
    elif command_name == "proceed_to_checkout":
        proceed_to_checkout()
    elif command_name == "fill_form_field":
        fill_form_field(params[0], params[1])
    elif command_name == "submit_form":
        submit_form()
    else:
        print(f"Unknown command: {command}")
    # Add more command handling as needed
    # ...existing code...