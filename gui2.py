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
        self.root.title("C2S Ai assistant DEMO")
        self.bot_message = ""
        self.message = ""
        self.is_listening = False

        self.canvas = tk.Canvas(root, width=600, height=400)
        self.canvas.pack()

        # Draw the gradient background
        for i in range(400):
            color = "#{:02x}{:02x}{:02x}".format(255, int(192 - i/2.5), int(203 - i/2.5))  # Gradient from pink to lighter pink
            self.canvas.create_rectangle(0, i, 600, i + 1, fill=color, outline=color)

        # Set the pink gradient background
        #self.root.configure(bg="#62E5FF")

         # Create a custom style for the labels with the desired background and text colors
        style = ttk.Style()
        style.configure("Custom.TLabel", background="#F5E3E0", foreground="black", font=("Arial", 12, "bold"), anchor="center")

        # Create the UI elements on the canvas
        self.label = ttk.Label(self.canvas, text="We're taking your order:", style="Custom.TLabel")
        self.label.place(x=200, y=50, width=200)

        self.user_text = ttk.Label(self.canvas, text="", style="Custom.TLabel", wraplength=500)
        self.user_text.place(x=50, y=100, width=500)

        self.output_label = ttk.Label(self.canvas, text="Your assisant says:", style="Custom.TLabel")
        self.output_label.place(x=200, y=200, width=200)

        self.bot_text = ttk.Label(self.canvas, text="", style="Custom.TLabel", wraplength=500)
        self.bot_text.place(x=50, y=250, width=500)

        self.submit_button = ttk.Button(self.canvas, text="Start", command=self.toggle_listening, style="Custom.TButton")
        self.submit_button.place(x=250, y=350, width=100)



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
                    self.user_text.config(text=f"You: {self.message}")
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
        self.bot_text.config(text="")
        for response in responses:
            self.bot_text.config(text=self.bot_text.cget("text") + f"Bot: {response}\n")
            self.text_to_speech(response)

    def text_to_speech(self, text):
        self.engine.say(text)
        self.engine.runAndWait()


if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceBotApp(root)
    root.mainloop()
