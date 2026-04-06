import threading
from config import HOST, PORT, ASSISTANT_NAME, USER_NAME, GEMINI_API_KEY
from voice.speaker import speak
from voice.listener import listen_once
from brain.gemini_client import ask
from brain.actions import execute
from server.app import start as start_server

def voice_loop():
    """
    Runs forever in the background.
    Listens to your mic, sends to Gemini, speaks the answer.
    Say 'jarvis' somewhere in your sentence to activate.
    """
    speak("Voice mode is active. I am listening for your commands.", block=True)

    while True:
        text = listen_once(timeout=10)

        if text is None:
            continue

        # Only respond if user said 'jarvis' or it's a long sentence
        if "jarvis" not in text.lower() and len(text.split()) < 3:
            continue

        print(f"\n[You]: {text}")
        raw    = ask(text)
        result = execute(raw)
        speak(result["spoken"])

        if result.get("result"):
            print(f"[System result]: {result['result']}")

def main():
    # Safety check — make sure API key is set
    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_KEY_HERE":
        print("=" * 50)
        print("ERROR: You forgot to add your Gemini API key!")
        print("Open config.py and paste your key on line 4.")
        print("=" * 50)
        return

    print(f"""
╔══════════════════════════════════════════╗
║   {ASSISTANT_NAME} — Personal AI Assistant          ║
║   Powered by Google Gemini 2.0 Flash     ║
╠══════════════════════════════════════════╣
║   Dashboard  →  http://localhost:{PORT}      ║
║   Voice      →  active (say 'Jarvis...')  ║
║   Stop       →  Ctrl + C                 ║
╚══════════════════════════════════════════╝
    """)

    speak(
        f"Good day {USER_NAME}. {ASSISTANT_NAME} is now online. "
        f"All systems are operational. How can I help you?",
        block=True
    )

    # Start voice loop in background so it doesn't block the server
    voice_thread = threading.Thread(target=voice_loop, daemon=True)
    voice_thread.start()

    # Start Flask web server — this keeps the program alive
    print(f"[Server] Dashboard running at http://localhost:{PORT}")
    start_server(host=HOST, port=PORT)

if __name__ == "__main__":
    main()