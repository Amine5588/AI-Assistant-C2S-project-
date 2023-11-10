# app.py
from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rasa_webhook', methods=['POST'])
def rasa_webhook():
    data = request.get_json()
    message = data['message']

    # Send user message to Rasa server and get the bot response
    try:
        rasa_response = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": message}).json()

        # Extract all the bot's response texts and concatenate them into a single string
        bot_responses = [response['text'] for response in rasa_response]
        bot_response = '\n'.join(bot_responses) if bot_responses else 'Sorry, I could not understand.'
    except requests.exceptions.RequestException as e:
        # Handle Rasa server connection errors
        bot_response = 'Oops! Something went wrong. Please try again later.'

    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
