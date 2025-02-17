from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

PROPS_FILE = 'template_props.json'

def load_props():
    if os.path.exists(PROPS_FILE):
        with open(PROPS_FILE, 'r') as f:
            return json.load(f)
    return {
        "title": "Welcome to My Template",
        "description": "This is a sample description",
        "features": ["Feature 1", "Feature 2", "Feature 3"],
        "showCTA": True,
        "ctaText": "Click Me"
    }

def save_props(props):
    with open(PROPS_FILE, 'w') as f:
        json.dump(props, f, indent=2)
    # Emit WebSocket event when props are updated
    socketio.emit('props_updated', props)

@app.route('/')
def index():
    props = load_props()
    return render_template('index.html', **props)

@app.route('/api/props', methods=['GET'])
def get_props():
    return jsonify(load_props())

@app.route('/api/props', methods=['POST'])
def update_props():
    props = request.json
    save_props(props)
    return jsonify({"status": "success"})

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('props_updated', load_props())

if __name__ == '__main__':
    socketio.run(
        app,
        debug=True,
        allow_unsafe_werkzeug=True,
    )  # For development only
