from flask import Flask, jsonify
from flask_cors import CORS
import status_checker

app = Flask(__name__)
CORS(app)

@app.route('/health')
def health_check():
    return jsonify(status="up")

@app.route('/api/status', methods=['GET'])
def get_status():
    # Use the results from the status_checker.py
    results = status_checker.results
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
