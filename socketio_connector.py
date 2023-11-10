import logging
from sanic import Blueprint, response, Sanic
from socketio import AsyncServer
from typing import Optional, Text, Any, Dict

import speech_recognition as sr
from pyttsx3 import init

from rasa.core.channels.channel import InputChannel
from rasa.core.channels.channel import UserMessage, OutputChannel


class SocketBlueprint(Blueprint):
    def __init__(
        self, sio: AsyncServer, socketio_path: Text, *args: Any, **kwargs: Any
    ) -> None:
        """Creates a :class:`sanic.Blueprint` for routing socketio connenctions.

        :param sio: Instance of :class:`socketio.AsyncServer` class
        :param socketio_path: string indicating the route to accept requests on.
        """
        super().__init__(*args, **kwargs)
        self.ctx.sio = sio
        self.ctx.socketio_path = socketio_path

    def register(self, app: Sanic, options: Dict[Text, Any]) -> None:
        """Attach the Socket.IO webserver to the given Sanic instance.

        :param app: Instance of :class:`sanic.app.Sanic` class
        :param options: Options to be used while registering the
            blueprint into the app.
        """
        self.ctx.sio.attach(app, self.ctx.socketio_path)
        super().register(app, options)


class SocketIOOutput(OutputChannel):
    @classmethod
    def name(cls):
        return "socketio"

    def __init__(self, sio, sid, bot_message_evt, message):
        self.sio = sio
        self.sid = sid
        self.bot_message_evt = bot_message_evt
        self.message = message

    async def _send_audio_message(self, socket_id, response, **kwargs: Any):
        # Get the bot's response from the Rasa model
        bot_response = response['text']

        # Use pyttsx3 to convert the response to speech
        engine = init()
        engine.say(bot_response)
        engine.runAndWait()


class SocketIOInput(InputChannel):
    @classmethod
    def name(cls):
        return "socketio"

    @classmethod
    def from_credentials(cls, credentials):
        return cls(credentials.get("user_message_evt", "user_uttered"),
                   credentials.get("bot_message_evt", "bot_uttered"),
                   credentials.get("namespace"),
                   credentials.get("session_persistence", False),
                   credentials.get("socketio_path", "/socket.io"),
                   )

    def __init__(self,
                 user_message_evt: Text = "user_uttered",
                 bot_message_evt: Text = "bot_uttered",
                 namespace: Optional[Text] = None,
                 session_persistence: bool = False,
                 socketio_path: Optional[Text] = '/socket.io'
                 ):
        self.bot_message_evt = bot_message_evt
        self.session_persistence = session_persistence
        self.user_message_evt = user_message_evt
        self.namespace = namespace
        self.socketio_path = socketio_path

    def blueprint(self, on_new_message):
        sio = AsyncServer(async_mode="sanic")
        socketio_webhook = SocketBlueprint(
            sio, self.socketio_path, "socketio_webhook", __name__
        )

        # ... Existing code ...

        @sio.on('user_uttered', namespace=self.namespace)
        async def handle_message(sid, data):
            output_channel = SocketIOOutput(sio, sid, self.bot_message_evt, data['message'])
            if data['message'] == "/get_started":
                message = data['message']
            else:
                # receive audio using the SpeechRecognition library
                r = sr.Recognizer()
                with sr.AudioFile(data['message']) as source:
                    audio = r.record(source)

                # Convert the user's audio to text using the SpeechRecognition library
                message = r.recognize_google(audio)

                await sio.emit(self.user_message_evt, {"text": message}, room=sid)

            message_rasa = UserMessage(message, output_channel, sid, input_channel=self.name())
            await on_new_message(message_rasa)

        return socketio_webhook
