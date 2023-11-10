import requests
import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()

bot_message = ""
message = ""

while bot_message.lower() not in ["bye", "thanks"]:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak Anything:")
        audio = r.listen(source)
        try:
            message = r.recognize_google(audio)
            print("You said:", message)
        except:
            print("Sorry, could not recognize your voice")

    if not message.strip():
        continue

    print("Sending message now...")
    r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": message})

    print("Bot says:")
    for i in r.json():
        bot_message = i['text']
        print(bot_message)

    # Use pyttsx3 for text-to-speech and play the audio directly
    engine.say(bot_message)
    engine.runAndWait()
