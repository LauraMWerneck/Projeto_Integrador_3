from flask import Flask, request, jsonify

app = Flask(__name__)  # Inicializa o aplicativo Flask, que será usado para criar a API

# Define a rota '/receive_data' que aceita apenas requisições POST
@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json  # Obtém os dados JSON enviados na requisição
    if not data:  # Verifica se os dados são válidos (não nulos)
        return jsonify({"error": "Dados inválidos"}), 400  # Retorna um erro 400 se os dados forem inválidos
    
    # Extrai os valores das chaves específicas no JSON recebido
    flow_rate = data.get("flow_rate")  # Vazão de água em L/min
    total_volume = data.get("total_volume")  # Volume total acumulado em litros
    distance = data.get("distance")  # Distância medida pelo sensor ultrassônico em cm

    # Exibe os dados recebidos no console
    print(f"Vazão: {flow_rate} L/min, Volume Total: {total_volume} L, Distância: {distance} cm")
    
    # Retorna uma resposta JSON indicando sucesso
    return jsonify({"status": "success"}), 200

# Executa o aplicativo Flask quando o script é iniciado
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Faz o servidor ouvir em todas as interfaces na porta 5000
