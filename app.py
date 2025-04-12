from flask import Flask, jsonify
import status_checker

app = Flask(__name__)

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
