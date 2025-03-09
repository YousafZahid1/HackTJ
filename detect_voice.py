import speech_recognition as sr
import commands as co

def detect_voice():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    try:
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

                    return text

                except sr.UnknownValueError:
                    print("Sorry, I could not understand the audio.")
                except sr.RequestError:
                    print("Sorry, there was an error with the speech recognition service.")
                except Exception as e:
                    print(f"An error occurred: {e}")
    except AttributeError:
        print("PyAudio is not installed. Please install it to use voice recognition.")