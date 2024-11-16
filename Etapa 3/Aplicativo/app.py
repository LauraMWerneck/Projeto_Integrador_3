from flask import Flask, request, jsonify
from flask_cors import CORS  # Importação do flask-cors

app = Flask(__name__)
CORS(app)  # Ativa o CORS para o app Flask

@app.route('/save_data', methods=['POST'])
def save_data():
    data = request.json
    consumo_hidrometro = data.get('consumoHidrometro')
    custo_agua = data.get('custoAgua')

    if consumo_hidrometro is None or custo_agua is None:
        return jsonify({'error': 'Dados inválidos!'}), 400

    # Log para verificar os dados recebidos
    print(f"Consumo registrado: {consumo_hidrometro} m³")
    print(f"Custo total: R$ {custo_agua}")

    return jsonify({'message': 'Dados recebidos com sucesso!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
