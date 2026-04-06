from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from brain.gemini_client import ask, reset_chat
from brain.actions import execute, get_system_stats
from voice.speaker import speak as jarvis_speak

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def index():
    """Serve the dashboard when you open http://localhost:5000"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """The dashboard sends messages here."""
    data         = request.json or {}
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({"error": "empty message"}), 400

    raw_response = ask(user_message)
    result       = execute(raw_response)

    jarvis_speak(result["spoken"])

    return jsonify({
        "response":      raw_response,
        "spoken":        result["spoken"],
        "action_result": result.get("result"),
        "type":          result["type"]
    })

@app.route('/system', methods=['GET'])
def system():
    """The dashboard polls this every 3 seconds for system stats."""
    return jsonify(get_system_stats())

@app.route('/clear', methods=['POST'])
def clear():
    """Clear JARVIS memory."""
    reset_chat()
    return jsonify({"status": "cleared"})

def start(host='0.0.0.0', port=5000):
    app.run(host=host, port=port, debug=False, use_reloader=False)