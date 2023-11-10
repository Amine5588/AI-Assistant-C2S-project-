import tkinter as tk
from tkinter import ttk
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

      
        self.canvas = tk.Canvas(root, width=600, height=400)
        self.canvas.pack()

        # Draw the gradient background
        for i in range(400):
            color = "#{:02x}{:02x}{:02x}".format(255, int(192 - i/2.5), int(203 - i/2.5))  # Gradient from pink to lighter pink
            self.canvas.create_rectangle(0, i, 600, i + 1, fill=color, outline=color)

        # Create a custom style for the labels with complementary background and readable text colors
        style = ttk.Style()
        style.configure("Custom.TLabel", background="#89CFF0", foreground="white", font=("Arial", 12, "bold"), anchor="center")

        # Create the UI elements on the canvas
        self.label = ttk.Label(self.canvas, text="Speak Anything:", style="Custom.TLabel")
        self.label.place(x=50, y=50, width=200, height=50)

        self.user_text = ttk.Label(self.canvas, text="", style="Custom.TLabel", wraplength=500)
        self.user_text.place(x=50, y=100, width=500, height=50)

        self.output_label = ttk.Label(self.canvas, text="Bot says:", style="Custom.TLabel")
        self.output_label.place(x=50, y=200, width=200, height=50)

        self.bot_text = ttk.Label(self.canvas, text="", style="Custom.TLabel", wraplength=500)
        self.bot_text.place(x=50, y=250, width=500, height=50)

        # Load the microphone image and create a Label to display the image as a clickable button
        self.microphone_image = tk.PhotoImage(file="C:/Users/Garaw/Desktop/C2S/init/mic.jpg")  # Replace "microphone.png" with the actual image filename
        self.microphone_button = tk.Label(self.canvas, image=self.microphone_image, bg="#89CFF0")
        self.microphone_button.place(x=250, y=350)  # Adjust the position as needed

        # Bind a click event to the microphone image button and associate the callback function
        self.microphone_button.bind("<Button-1>", self.on_microphone_click)

        # Initialize the text-to-speech engine
        self.engine = pyttsx3.init()

    def on_microphone_click(self, event):
        # This function will be executed when the microphone image button is clicked
        self.toggle_listening()

    def toggle_listening(self):
        self.is_listening = not self.is_listening
        if self.is_listening:
            self.microphone_button.config(image="", text="Listening", font=("Arial", 12, "bold"))
            threading.Thread(target=self.start_listening).start()
        else:
            self.microphone_button.config(image=self.microphone_image, text="")
            self.submit_button.config(text="Submit")

    # ... Rest of the class methods ...


if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceBotApp(root)
    root.mainloop()
