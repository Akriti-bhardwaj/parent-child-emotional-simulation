from flask import Flask, jsonify, send_from_directory
import random

# Initialize Flask app
app = Flask(__name__, static_folder='static')

# Define the FamilyMember class
class FamilyMember:
    def __init__(self, name, stress):
        self.name = name
        self.stress = stress

# Create Parent and Child objects
family = {
    "Parent": FamilyMember("Parent", 60),
    "Child": FamilyMember("Child", 40)
}

# Define possible daily emotional events
events = [
    {"event": "Good day at study", "parent_delta": -5, "child_delta": -10},
    {"event": "Argument over study hours", "parent_delta": +15, "child_delta": +20},
    {"event": "Encouraging talk", "parent_delta": -10, "child_delta": -15},
    {"event": "Exam stress increases", "parent_delta": +10, "child_delta": +15},
    {"event": "Parent feels anxious for child", "parent_delta": +8, "child_delta": +5},
    {"event": "Shared family time", "parent_delta": -8, "child_delta": -10},
    {"event": "Support and empathy shown", "parent_delta": -12, "child_delta": -12},
    {"event": "Overexpectation from parent", "parent_delta": +20, "child_delta": +25},
    {"event": "Relaxation or break", "parent_delta": -5, "child_delta": -5},
    {"event": "Neutral day", "parent_delta": 0, "child_delta": 0}
]

def clamp(value, low=0, high=100):
    return max(low, min(high, value))

def update_emotions():
    """Applies a random emotional event and updates stress levels."""
    event = random.choice(events)
    family["Parent"].stress = clamp(family["Parent"].stress + event["parent_delta"])
    family["Child"].stress = clamp(family["Child"].stress + event["child_delta"])
    return event

def get_state():
    """Returns current emotional state as JSON."""
    return {
        "Parent": {"stress": family["Parent"].stress},
        "Child": {"stress": family["Child"].stress}
    }

# Serve index.html
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    event = update_emotions()
    return jsonify({"state": get_state(), "event": event})

@app.route('/get_state', methods=['GET'])
def get_current_state():
    return jsonify(get_state())

@app.route('/reset', methods=['POST'])
def reset():
    family["Parent"].stress = 60
    family["Child"].stress = 40
    return jsonify({"message": "Simulation reset!", "state": get_state()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
