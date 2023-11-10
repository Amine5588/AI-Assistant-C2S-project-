import requests
import speech_recognition as sr
import pyttsx3
import threading

class VoiceBot:
    def __init__(self):
        self.bot_message = ""
        self.message = ""
        self.is_listening = False

        # Initialize the text-to-speech engine
        self.engine = pyttsx3.init()

    def toggle_listening(self):
        self.is_listening = not self.is_listening
        if self.is_listening:
            threading.Thread(target=self.start_listening).start()
        else:
            print("Stopped listening.")
            self.is_listening = False

    def start_listening(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            while self.is_listening:
                audio = r.listen(source)

                try:
                    self.message = r.recognize_google(audio)
                    print(f"You: {self.message}")
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
            print(f"Bot: {bot_response}")
            bot_responses.append(bot_response)

        self.text_to_speech(bot_responses)

    def text_to_speech(self, texts):
        for text in texts:
            self.engine.say(text)
            self.engine.runAndWait()


if __name__ == "__main__":
    bot = VoiceBot()
    print("Voice bot is running. Press Enter to start listening or type 'exit' to quit.")
    while True:
        command = input()
        if command.lower() == 'exit':
            break
        elif not bot.is_listening:
            bot.toggle_listening()
    print("Goodbye!")
    