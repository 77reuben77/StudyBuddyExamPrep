from chatbot import Chatbot
from chatbot import Database
from chatbot import WhatsAppGraphAPI, convert_mathpix, OpenAIAPI
import json
import hashlib
import hmac
from flask import jsonify
import threading
from flask import Flask, request, jsonify


###################################################################


app = Flask(__name__)


@app.route('/handle_webhook', methods=['POST'])
def handle_webhook():
    data = json.loads(request.data.decode('utf-8'))

    message_text = ''
    entry = data.get("entry")[0]
    changes = entry.get("changes")[0]
    value = changes.get("value")

    messages = value.get("messages")
    if messages:
        print(data)
        messages = value.get("messages")[0]

        phone_number = messages.get("from")
        message_type = messages.get("type")

        whatsapp_media_instance = WhatsAppGraphAPI(phone_number)

        if message_type == "text":
            message_text = messages.get("text").get("body")

        elif message_type == "interactive":
            message_text = messages.get("interactive").get("button_reply").get("id")
        elif message_type == "image":
            print(data)
            image_data = messages.get("image")
            image_id = image_data.get("id")
            mime_type = image_data.get("mime_type")
            image_caption = image_data.get("caption")
            image_path = whatsapp_media_instance.download_media(image_id, image_id, mime_type)
            print(image_path)
            image_text = convert_mathpix(image_path)
            message_text = f"{image_text}\n\n{image_caption}"
            print(message_text)

        elif message_type == "audio":
            audio_data = messages.get("audio")
            audio_id = audio_data.get("id")
            mime_type = audio_data.get("mime_type")
            audio_path = whatsapp_media_instance.download_media(audio_id, audio_id, mime_type)
            message_text = OpenAIAPI.transcribe_audio(audio_path)

        t_chatbot = Chatbot(message_text, message_type, phone_number)
        t_chatbot.process_message()

        return 'OK', 200
    else:
        return 'OK', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=65000)
