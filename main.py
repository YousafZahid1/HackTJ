import google.generativeai as genai
import commands as com
import os
import re
import pyautogui
from detect_voice import detect_voice
from requests import *
def get_user_input():
    user_input = input("Type something: ")
    return user_input

def capture_screen():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    return "screenshot.png"

def capture_screen_region(region):
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save("screenshot_region.png")
    return "screenshot_region.png"

def generate_ai_response(text, region=None):
    genai.configure(api_key="AIzaSyDNTQ95A2eub-4DS9vIHzeMO0o7sn2EmzI")
    model = genai.GenerativeModel("gemini-1.5-flash")
    # screenshot_path = capture_screen_region(region) if region else capture_screen()
    # with open(screenshot_path, "rb") as image_file:
    #     image_data = image_file.read()
    # print(f"Image data length: {len(image_data)}")  # Debugging statement
    try:
        response = model.generate_content(text)  # Removed image argument
        print(f"AI response: {response}")  # Debugging statement
        return response.text
    except Exception as e:
        print(f"Error generating AI response: {e}")  # Debugging statement
        return "Error generating AI response"

def parse_ai_response(response):
    # Extract the commands from the AI response
    pattern = re.compile(r'\[(.*?)\]', re.DOTALL)
    match = pattern.search(response)
    if match:
        commands_str = match.group(1)
        commands_list = [cmd.strip() for cmd in commands_str.split('),') if cmd]
        commands_list = [cmd + ')' if not cmd.endswith(')') else cmd for cmd in commands_list]
        return commands_list
    return []

if __name__ == "__main__":
    while True:
        # user_input = detect_voice()
        user_input = get_user_input()  # Simulate voice input with user input for debugging
        if user_input == "exit":
            print("Exiting...")
            break
        ai_response = generate_ai_response("""For the next responses, interpret the user input and give me a set of plain text commands 
                            that will implement the user request. The commands should be in the format (no quotations):
                             [command1(param1, ...), command2(param1, ...], ...]. Give me the commands only from this list:
                             move_mouse(x, y), click_mouse(), double_click_mouse(), scroll_mouse(amount), drag_mouse(x, y),
                             open_website(domain), find_button(button), navigate_to_section(section), write_text(text),
                             wait(seconds), capture_region(x, y, width, height), search_product(query), select_product(image_path),
                             add_to_cart(), proceed_to_checkout(), fill_form_field(field, value), submit_form()
                             Make sure to note that sites take 3s to load. Here is the input:""" + user_input)
        print(ai_response)
        commands = parse_ai_response(ai_response)
        for command in commands:
            com.execute_command(command)
