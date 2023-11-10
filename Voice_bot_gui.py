import tkinter as tk
from tkinter import ttk
import tkinter.font
import requests
import speech_recognition as sr
import pyttsx3
import threading

class VoiceBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Bot")
        self.bot_message = ""
        self.message = ""
        self.is_listening = False
        
        
        # Create the UI elements
        self.label = ttk.Label(root, text="Speak Anything:")
        self.label.pack(pady=10)
        
        self.user_text = tk.Text(root, height=5, width=60)
        self.user_text.pack(pady=5)

        self.output_label = ttk.Label(root, text="Bot says:")
        self.output_label.pack(pady=5)
        
        self.bot_text = tk.Text(root, height=5, width=60, state=tk.DISABLED)
        self.bot_text.pack(pady=5)
        
        self.submit_button = ttk.Button(root, text="Submit", command=self.toggle_listening)
        self.submit_button.pack(pady=5)


        # Initialize the text-to-speech engine
        self.engine = pyttsx3.init()

    def toggle_listening(self):
        self.is_listening = not self.is_listening
        if self.is_listening:
            self.submit_button.config(text="Stop Listening")
            threading.Thread(target=self.start_listening).start()
        else:
            self.submit_button.config(text="Submit")

    def start_listening(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            while self.is_listening:
                print("Listening...")
                audio = r.listen(source)

                try:
                    self.message = r.recognize_google(audio)
                    self.user_text.delete("1.0", tk.END)
                    self.user_text.insert(tk.END, f"You: {self.message}\n")
                    #self.text_to_speech(f"You said: {self.message}")
                    self.send_request_to_rasa()
                except sr.UnknownValueError:
                    self.text_to_speech("Sorry, could not recognize your voice")
                except sr.RequestError:
                    self.text_to_speech("Could not request results; please check your internet connection.")

    def send_request_to_rasa(self):
        if not self.message.strip():
            return

        print("Sending message now...")
        r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": self.message})

        bot_responses = []
        for i in r.json():
            bot_response = i['text']
            print(bot_response)
            bot_responses.append(bot_response)

        self.display_bot_response(bot_responses)

    def display_bot_response(self, responses):
        self.bot_text.config(state=tk.NORMAL)
        self.bot_text.delete("1.0", tk.END)
        for response in responses:
            self.bot_text.insert(tk.END, f"Bot: {response}\n")
            self.text_to_speech(response)
        self.bot_text.config(state=tk.DISABLED)
        self.bot_text.see(tk.END)

    def text_to_speech(self, text):
        self.engine.say(text)
        self.engine.runAndWait()


if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceBotApp(root)
    root.mainloop()
