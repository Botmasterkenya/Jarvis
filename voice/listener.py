import speech_recognition as sr
from config import SPEECH_LANGUAGE

recognizer = sr.Recognizer()
recognizer.pause_threshold  = 0.8
recognizer.energy_threshold = 300

def listen_once(timeout: int = 8, phrase_limit: int = 15):
    """
    Listen from your microphone.
    Returns the text you said, or None if nothing was heard.
    """
    with sr.Microphone() as source:
        print("[JARVIS] Adjusting for background noise...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("[JARVIS] Listening... speak now")
        try:
            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_limit
            )
            text = recognizer.recognize_google(audio, language=SPEECH_LANGUAGE)
            print(f"[You said]: {text}")
            return text
        except sr.WaitTimeoutError:
            print("[JARVIS] No speech heard.")
            return None
        except sr.UnknownValueError:
            print("[JARVIS] Could not understand. Try again.")
            return None
        except sr.RequestError as e:
            print(f"[JARVIS] Speech service error: {e}")
            return None