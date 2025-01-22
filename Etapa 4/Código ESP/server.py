from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json
    if not data:
        return jsonify({"error": "Dados inválidos"}), 400
    
    flow_rate = data.get("flow_rate")
    total_volume = data.get("total_volume")
    
    print(f"Vazão: {flow_rate} L/min, Volume Total: {total_volume} L")
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
