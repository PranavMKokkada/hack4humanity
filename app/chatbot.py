from flask import Blueprint, request, jsonify
from gtts import gTTS
import openai
import os

# Set OpenAI API key
openai.api_key = "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"

# Create a blueprint for the chatbot functionality
chatbot_app = Blueprint('chatbot', __name__)

# Function for text-to-speech using gTTS
def speak(text):
    tts = gTTS(text)
    tts.save("response.mp3")  # Save the audio file
    os.system("mpg321 response.mp3")  # Or use any media player to play the audio

@chatbot_app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"response": "Please send a valid message."})

    try:
        # Get a response from OpenAI
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"User: {user_message}\nAssistant:",
            max_tokens=150,
            n=1,
            stop=["User:", "Assistant:"]
        )
        
        bot_reply = response.choices[0].text.strip()

        # Use gTTS to convert bot's reply to speech
        speak(bot_reply)  # This will play the audio response

        return jsonify({"response": bot_reply})
    
    except Exception as e:
        return jsonify({"response": "An error occurred with the chatbot."})
