from flask import Flask, jsonify
from flask_cors import CORS
import socket
import time

app = Flask(__name__)
CORS(app)

# Function to check TCP status for a server
def check_tcp(host, port):
    start = time.time()
    try:
        sock = socket.create_connection((host, port), timeout=5)
        latency = round((time.time() - start) * 1000, 2)
        sock.close()
        return True, latency
    except:
        return False, None

# List of servers to check
servers = {
    "Core Chat (c3.whatsapp.net:5222)": ("c3.whatsapp.net", 5222),
    "Core Chat (c4.whatsapp.net:5222)": ("c4.whatsapp.net", 5222),
    "Core Chat (e1.whatsapp.net:5222)": ("e1.whatsapp.net", 5222),
    "Core Chat (g.whatsapp.net:5222)": ("g.whatsapp.net", 5222),
    "Media (mmg.whatsapp.net:443)": ("mmg.whatsapp.net", 443),
    "Media (media.whatsapp.net:443)": ("media.whatsapp.net", 443),
    "Media CDN (media-mxp1-1.cdn.whatsapp.net:443)": ("media-mxp1-1.cdn.whatsapp.net", 443),
    "Media CDN (mmx-ds.cdn.whatsapp.net:443)": ("mmx-ds.cdn.whatsapp.net", 443),
    "Media Content (scontent.whatsapp.net:443)": ("scontent.whatsapp.net", 443),
    "Static Assets (static.whatsapp.net:443)": ("static.whatsapp.net", 443),
    "WhatsApp Web (web.whatsapp.com:443)": ("web.whatsapp.com", 443),
    "Main Website (www.whatsapp.com:443)": ("www.whatsapp.com", 443),
    "FAQ & Help (faq.whatsapp.com:443)": ("faq.whatsapp.com", 443),
    "Group Invite Links (chat.whatsapp.com:443)": ("chat.whatsapp.com", 443),
    "Misc Server (dit.whatsapp.net:443)": ("dit.whatsapp.net", 443),
    "Maybe Blocked? (e6.whatsapp.net:5222)": ("e6.whatsapp.net", 5222),
}

@app.route('/health')
def health_check():
    return jsonify(status="up")

@app.route('/api/status', methods=['GET'])
def get_status():
    results = {}
    
    # Perform the TCP check for each server on request
    for name, (host, port) in sorted(servers.items()):
        status, latency = check_tcp(host, port)
        
        # Determine the status text and level
        if status:
            status_text = "UP"
            status_level = "good" if latency < 300 else "warn"
        else:
            status_text = "DOWN"
            status_level = "bad"
            latency = None
        
        # Save the status information for this server
        results[name] = {
            "host": host,
            "port": port,
            "status": status_text,
            "level": status_level,
            "latency": latency if latency is not None else "N/A"
        }
    
    # Return the updated status data as JSON
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

