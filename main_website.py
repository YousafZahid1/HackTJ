import cv2
import mediapipe as mp
import pyautogui
import speech_recognition as sr
#import website_open as wo  # Assuming website_open is inside this module
import threading
import queue
import commands as com
import detect_voice as dv
import ast
import re
import google.generativeai as genai
import commands as com
import detect_voice as dv
import re
import webbrowser
from collections import deque
import numpy as np

def website_opener(domain):
    try:
        domain = domain.lower().replace(" ", "")
        url = f'https://www.{domain}.com'
        
        webbrowser.open(url)
        return True
    except Exception as e:
        print(e)
        return False

frame_queue = queue.Queue()

def detect_voice():
   # Initialize the recognizer
   recognizer = sr.Recognizer()
   counter = 0


   # Use the microphone as the audio source
   with sr.Microphone() as source:
       print("Adjusting for ambient noise... Please wait.")
       recognizer.adjust_for_ambient_noise(source, duration=1)
       print("Listening for commands...")


       while True:  # Continuous loop to listen for commands
           try:
               print("Listening...")
               audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)  # Capture the audio with reduced timeout and phrase_time_limit


               # Use Google's speech recognition engine
               text = recognizer.recognize_google(audio).lower()
               print(f"Detected voice input: {text}")


               # Check for commands
               if 'hello' in text:
                   print("Hello! How can I assist you?")
               elif 'open' in text:
                   # Extract the website name after 'open'
                   if text == 'open':
                       continue
                   site = text.split('open ')[-1].strip()
                   if site:
                       print(f"Opening {site}...")
                       website_opener(site)  # Use the website opener function
                   else:
                       print("Sorry, I couldn't understand the website name.")
               elif 'exit' in text:
                   print("Goodbye!") 
                   break  # Exit the loop and stop the program
               else:
                   counter = counter + 1
                   print("Unkown command.")
                   recognizer.adjust_for_ambient_noise(source, duration=.1)
                  
                   if counter > 5:
                       print ("Too many errors, quitting.")
                       break


           except sr.UnknownValueError:
               print("Sorry, I could not understand the audio.")
           except sr.RequestError:
               print("Sorry, there was an error with the speech recognition service.")
           except Exception as e:
               print(f"An error occurred: {e}")




def eye_tracking(sensitivity=2.0, smoothing_factor=10):
    cam = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    screen_w, screen_h = pyautogui.size()
    pyautogui.moveTo(screen_w // 2, screen_h // 2)
    
    # Smoothing buffer
    position_buffer = deque(maxlen=smoothing_factor)
    
    # Scroll parameters
    SCROLL_THRESHOLD_UP = -0.09  # Adjusted threshold for scrolling up
    SCROLL_THRESHOLD_DOWN = -0.13  # Adjusted threshold for scrolling down
    SCROLL_AMOUNT = 1  # Further reduced scroll amount for slower scrolling
    
    # Dead zone to prevent jitter
    DEAD_ZONE = 0.02
    
    while cam.isOpened():
        success, frame = cam.read()
        if not success:
            break
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape
        
        if landmark_points:
            landmarks = landmark_points[0].landmark
            
            # Use more stable eye center points (left: 468, right: 473)
            left_eye_center = landmarks[468]  # Left eye pupil
            right_eye_center = landmarks[473] # Right eye pupil
            
            # Calculate average eye position
            eye_x = (left_eye_center.x + right_eye_center.x) / 2
            eye_y = (left_eye_center.y + right_eye_center.y) / 2
            
            # Normalize coordinates (0.5 is center)
            norm_x = eye_x - 0.5
            norm_y = eye_y - 0.5
            
            # Apply dead zone
            if abs(norm_x) < DEAD_ZONE:
                norm_x = 0
            if abs(norm_y) < DEAD_ZONE:
                norm_y = 0
            
            # Calculate screen position with sensitivity
            target_x = screen_w // 2 + norm_x * screen_w * sensitivity
            target_y = screen_h // 2 + norm_y * screen_h * sensitivity
            
            # Smooth the movement
            position_buffer.append((target_x, target_y))
            avg_x = np.mean([pos[0] for pos in position_buffer])
            avg_y = np.mean([pos[1] for pos in position_buffer])
            
            # Keep cursor within screen bounds
            avg_x = np.clip(avg_x, 0, screen_w)
            avg_y = np.clip(avg_y, 0, screen_h)
            
            pyautogui.moveTo(avg_x, avg_y)
            
            # Visualize eye centers
            for landmark in [left_eye_center, right_eye_center]:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 0))
            
            # Click detection using eye outer corners
            left_eye = [landmarks[145], landmarks[159]]
            right_eye = [landmarks[374], landmarks[386]]
            for landmark in left_eye + right_eye:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 255))
            
            left_eye_ratio = left_eye[0].y - left_eye[1].y
            right_eye_ratio = right_eye[0].y - right_eye[1].y
            if left_eye_ratio < 0.015 and right_eye_ratio > 0.015:
                pyautogui.click()
                pyautogui.sleep(1)
            
            # Scroll detection
            nose_y = landmarks[1].y
            avg_eye_y = (left_eye[0].y + left_eye[1].y + 
                        right_eye[0].y + right_eye[1].y) / 4
            eye_relative_pos = avg_eye_y - nose_y
            
            if eye_relative_pos > SCROLL_THRESHOLD_UP:
                print("Scrolling up")
                pyautogui.scroll(SCROLL_AMOUNT)
            elif eye_relative_pos < SCROLL_THRESHOLD_DOWN:
                print("Scrolling down")
                pyautogui.scroll(-SCROLL_AMOUNT)
                
        frame_queue.put(frame)
    cam.release()

def display_frames():
    cv2.namedWindow('Eye Controlled Mouse', cv2.WINDOW_NORMAL)
    screen_w, screen_h = pyautogui.size()
    cv2.moveWindow('Eye Controlled Mouse', screen_w // 2 - 320, screen_h // 2 - 240)  # Center the window
    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
            cv2.imshow('Eye Controlled Mouse', frame)
            print("Displaying frame")  # Debug print statement
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Frame queue is empty")  # Debug print statement
    cv2.destroyAllWindows()

def both(sensitivity):
    eye_tracking_thread = threading.Thread(target=eye_tracking, args=(sensitivity,))
    detect_voice_thread = threading.Thread(target=detect_voice)
    display_frames_thread = threading.Thread(target=display_frames)
    eye_tracking_thread.start()
    # detect_voice_thread.start()
    # display_frames_thread.start()
    func()




def func():


    def generate_ai_response(text, region=None):
        genai.configure(api_key="AIzaSyDNTQ95A2eub-4DS9vIHzeMO0o7sn2EmzI")
        model = genai.GenerativeModel("gemini-1.5-flash")
        try:
            response = model.generate_content(text)
            return response.text
        except Exception as e:
            print(f"Error generating AI response: {e}")  # Debugging statement
            return "Error generating AI response"
        
    def parse_ai_response(response):
        # Extract the commands from the AI response
        response = response.strip().strip('`')
        if not (response.startswith("[") and response.endswith("]")):
            response = f"[{response}]"
        pattern = re.compile(r'\[(.*?)\]', re.DOTALL)
        match = pattern.search(response)
        if match:
            commands_str = match.group(1)
            # Remove any extraneous newline characters
            commands_str = commands_str.replace('\n', '')
            commands_list = [cmd.strip() for cmd in commands_str.split('),') if cmd]
            commands_list = [cmd + ')' if not cmd.endswith(')') else cmd for cmd in commands_list]
            commands_list = [cmd.strip('[').strip(']') for cmd in commands_list]  # Remove leading `[` and trailing `]`
            return commands_list
        return []

    def loop():
        init_prompt = """For the next responses, interpret the user input and give me a set of plain text commands 
                        that will implement the user request. The commands should be in the format (no quotations):
                        [command1(param1, ...), command2(param1, ...), ...]. Give me the commands only from this list:
                        move_mouse(x, y), click(), double_click(), scroll_continuous(amount, duration=20), stop_scrolling(), open_website(domain), type(text), wait(seconds)
                        Make sure to note that sites take 3s to load. Here is the input:"""
        #print(generate_ai_response(init_prompt))
        
        while True:
            user_input = dv.detect_voice()
            if user_input == 'exit':
                break
            ai_response = generate_ai_response(init_prompt + user_input)
            print(f"AI response: {ai_response}")
            
            commands = parse_ai_response(ai_response)
            print(f"Commands: {commands}")
            
            for command in commands:
                com.execute_command(command)

    if __name__ == "__main__":
        loop()






import tkinter as tk
import random as r

##### SIGN UP PAGE #####

# Create the Login window
first = tk.Tk()
first.geometry("500x500")
first.title("Jefferson HELPER")

# Title Label
label = tk.Label(first, text="Jefferson Helper", font=('Bold', 28))
label.pack(padx=50, pady=30)

label = tk.Label(first, text="Your handy dandy helper", font=('Arial', 15))
label.place()

# Button for login
button = tk.Button(first, text="Enable Jefferson", font=('Bold', 15), command=detect_voice)
button.pack(pady=20)

# Sensitivity slider
sensitivity_var = tk.DoubleVar(value=4.0)  # Set default sensitivity to 4.0
slider = tk.Scale(first, from_=2.0, to=8.0, resolution=0.5, orient=tk.HORIZONTAL, label="Sensitivity", variable=sensitivity_var)
slider.pack(pady=20)

button = tk.Button(first, text="Enable Eye Tracker", font=('Bold', 15), command=lambda: eye_tracking(sensitivity_var.get()))
button.pack(pady=40)

button2 = tk.Button(first, text="Enable Eye Tracker & Enable Jefferson", font=('Bold', 15), command=lambda: both(sensitivity_var.get()))
button2.pack(pady=30)

# Run the Login window
first.mainloop()