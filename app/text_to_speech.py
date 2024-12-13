import pyttsx3

def text_to_speech(text):
    try:
        # Initialize the speech engine
        engine = pyttsx3.init()

        # Set properties (optional)
        rate = engine.getProperty('rate')  # Speed of speech
        print(f"Current rate: {rate}")
        engine.setProperty('rate', rate - 50)  # Adjust speech rate (optional)

        volume = engine.getProperty('volume')  # Volume (0.0 to 1.0)
        print(f"Current volume: {volume}")
        engine.setProperty('volume', 1)  # Set volume to maximum (optional)

        # Speak the text
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in text-to-speech conversion: {e}")

# Example usage
text_to_speech("Hello! This is a test of text to speech.")
