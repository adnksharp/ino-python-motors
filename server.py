from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/enc_status', methods=['POST'])
def receive_data():
    if request.is_json:
        data = request.get_json()
        print(f">> {data}")

        return jsonify({"status": "success", "message": "Data received", "voltage": 0}), 200
    else:
        return jsonify({"status": "error", "message": "Content-Type must be application/json"}), 400


if __name__ == '__main__':
    app.run(host='10.42.0.1')
