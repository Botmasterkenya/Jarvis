import subprocess
import threading
import pyttsx3
from config import TTS_RATE, TTS_PITCH, USE_ESPEAK

_tts_engine = None

def _get_engine():
    global _tts_engine
    if _tts_engine is None:
        _tts_engine = pyttsx3.init()
        _tts_engine.setProperty('rate', TTS_RATE * 10)
        voices = _tts_engine.getProperty('voices')
        if voices:
            _tts_engine.setProperty('voice', voices[0].id)
    return _tts_engine

def _speak_espeak(text: str):
    clean = (text
             .replace('"', '')
             .replace("'", "")
             .replace('\n', ' ')
             .replace('*', '')
             .replace('#', ''))
    subprocess.run(
        ["espeak-ng", "-s", str(TTS_RATE), "-p", str(TTS_PITCH), clean],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def _speak_pyttsx3(text: str):
    try:
        engine = _get_engine()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[Speaker] Error: {e}")

def speak(text: str, block: bool = False):
    """Speak text out loud. Non-blocking by default."""
    print(f"\n[JARVIS says]: {text}")
    fn = _speak_espeak if USE_ESPEAK else _speak_pyttsx3
    if block:
        fn(text)
    else:
        threading.Thread(target=fn, args=(text,), daemon=True).start()