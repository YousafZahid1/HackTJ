import cv2
import mediapipe as mp
import pyautogui
import speech_recognition as sr
import website_open as wo  # Assuming websiccte_opener is inside this module
import threading
import queue

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
                       wo.website_opener(site)  # Use the website opener function
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




def eye_tracking(sensitivity):
    cam = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    screen_w, screen_h = pyautogui.size()
    pyautogui.moveTo(screen_w // 2, screen_h // 2)  # Start cursor in the middle of the screen
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
            for id, landmark in enumerate(landmarks[474:478]):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 0))
                if id == 1:
                    screen_x = screen_w // 2 + (landmark.x - 0.5) * screen_w * sensitivity
                    screen_y = screen_h // 2 + (landmark.y - 0.5) * screen_h * sensitivity
                    pyautogui.moveTo(screen_x, screen_y)
            left_eye = [landmarks[145], landmarks[159]]
            right_eye = [landmarks[374], landmarks[386]]
            for landmark in left_eye + right_eye:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 255))
            left_eye_ratio = left_eye[0].y - left_eye[1].y
            right_eye_ratio = right_eye[0].y - right_eye[1].y
            
            if left_eye_ratio < 0.015 and right_eye_ratio > 0.015:  # Detect left eye wink
                pyautogui.click()
                pyautogui.sleep(1)
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
    detect_voice_thread.start()
    display_frames_thread.start()

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