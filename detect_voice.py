import speech_recognition as sr
import commands as co

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
                audio = recognizer.listen(source)  # Capture the audio

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
                        return f"open_website({site})"
                    else:
                        print("Sorry, I couldn't understand the website name.")
                elif 'capture region' in text:
                    # Extract the region coordinates after 'capture region'
                    coords = text.split('capture region ')[-1].strip()
                    if coords:
                        try:
                            x, y, width, height = map(int, coords.split())
                            print(f"Capturing region: {x}, {y}, {width}, {height}")
                            return f"capture_region({x}, {y}, {width}, {height})"
                        except ValueError:
                            print("Invalid coordinates format. Please provide four integers.")
                    else:
                        print("Sorry, I couldn't understand the region coordinates.")
                elif 'exit' in text:
                    print("Goodbye!")
                    return "exit"  # Exit the loop and stop the program
                else:
                    counter += 1
                    print("Unknown command.")
                    recognizer.adjust_for_ambient_noise(source, duration=.1)
                    
                    if counter > 5:
                        print("Too many errors, quitting.")
                        return "exit"

                return text

            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio.")
            except sr.RequestError:
                print("Sorry, there was an error with the speech recognition service.")
            except Exception as e:
                print(f"An error occurred: {e}")