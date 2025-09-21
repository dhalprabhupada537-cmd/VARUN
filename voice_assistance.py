import speech_recognition as sr
import pyttsx3,webbrowser
recognizer = sr.Recognizer()
engine = pyttsx3.init()
def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()
def listen_command():
    with sr.Microphone(device_index=1) as source:  
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.WaitTimeoutError:
            speak("No speech detected, please try again.")
        except sr.UnknownValueError:
            speak("Sorry, I could not understand.")
        except sr.RequestError:
            speak("Speech recognition service is down.")
    return ""
def process_command(command):
    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif command.strip() == "":
        pass  
    else:
        speak("Sorry, I don't know how to do that yet.")
if __name__ == "__main__":
    speak("Hello,user Say something...")
    while True:
        command = listen_command()
        if command:
            print("You said:", command)
            if "exit" in command or "quit" in command or "stop" in command:
                speak("Goodbye!")
                break
            process_command(command)
