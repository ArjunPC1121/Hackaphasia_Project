from googletrans import Translator
from gtts import gTTS


translator = Translator()

def translate_and_speak(text, target_language='kn'):  # Default to Kannada
    try:
        # Translate text
        translation = translator.translate(text, dest=target_language)
        
        # Check if translation is valid
        if translation is None or not translation.text:
            return "Error: Translation failed."

        translated_text = translation.text

        # Optionally, create a TTS object and save the audio (not required for this use case)
        tts = gTTS(text=translated_text, lang=target_language)
        tts.save("translation.mp3")

        # Optionally, play the audio (comment out if not needed)
        # os.system("mpg321 translation.mp3")  # Adjust this if needed for your system

        return translated_text

    except Exception as e:
        return f"Error: {e}"
