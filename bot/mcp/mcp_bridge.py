from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

incomes = [
   { 'description': 'salary', 'amount': 5000 }
]

@app.route('/incomes')
def get_incomes():
   return jsonify(incomes)

def start_bridge():
    socketio.run(app, port=8000, debug=False, use_reloader=False)