let recognition;

// Function to hide the greeting message when the "Start" button is clicked
function hideGreetingMessage() {
    const greetingMessageDiv = document.getElementById('greetingMessage');

    // Hide the greeting message
    greetingMessageDiv.style.display = 'none';

    // Continue with the rest of your logic
    // ... (existing JavaScript code) ...
}

// Add event listener to the "Start" button
document.getElementById('startButton').addEventListener('click', hideGreetingMessage);

// ... (existing JavaScript code) ...

function initSpeechRecognition() {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
        const loader = document.querySelector('.loader');
        loader.style.display = 'flex';
    };

    recognition.onend = () => {
        const loader = document.querySelector('.loader');
        loader.style.display = 'none';

        const startButton = document.getElementById('startButton');
        startButton.disabled = false;
    };

    recognition.onresult = (event) => {
        const message = event.results[0][0].transcript;
        console.log('You said:', message);
        if (message.trim() !== '') {
            const recognizedSpeechDiv = document.getElementById('recognizedSpeech');
            sendUserMessage(message, recognizedSpeechDiv);
        }
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
    };
}

function handleUserSpeech(event) {
    if (!recognition) {
        initSpeechRecognition();
    }

    const startButton = document.getElementById('startButton');
    startButton.disabled = true;

    // Hide the loader when starting speech recognition
    const loader = document.querySelector('.loader');
    loader.style.display = 'flex';

    recognition.start();
}

function sendUserMessage(message, recognizedSpeechDiv) {
    recognizedSpeechDiv.textContent = '';

  

    fetch('/rasa_webhook', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then((response) => response.json())
    .then((data) => {
        const botResponse = data.response;
        if (botResponse) {
            recognizedSpeechDiv.textContent = botResponse;
            const utterance = new SpeechSynthesisUtterance(botResponse);
            utterance.lang = 'en-US';
                       // Show the loader when speech starts
            

            speechSynthesis.speak(utterance);


        } else {
            recognizedSpeechDiv.textContent = 'Sorry, I could not understand.';
            //loader.style.display = 'flex';


        }
    })
    .catch((error) => {
        console.error('Error sending user message:', error);
    });
}

document.getElementById('startButton').addEventListener('click', handleUserSpeech);

// Add event listener to the recognition end event
if (recognition) {
    recognition.addEventListener('end', () => {
        const loader = document.querySelector('.loader');
        loader.style.display = 'none';

        const startButton = document.getElementById('startButton');
        startButton.disabled = false;
    });
}
