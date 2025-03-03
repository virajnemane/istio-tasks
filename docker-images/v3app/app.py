from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def get_client_ip():
    # Get real client IP from headers
    x_forwarded_for = request.headers.get('X-Forwarded-For', None)
    real_ip = request.remote_addr  # This is the real source IP seen by the server

    return jsonify({
        "X-Forwarded-For": x_forwarded_for,
        "Remote-Addr": real_ip
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9080, debug=True)
