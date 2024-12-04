from flask import Flask, request, jsonify
from flask_cors import CORS  # Importação do flask-cors
from datetime import datetime


app = Flask(__name__)
CORS(app)  # Ativa o CORS para o app Flask

# Variáveis globais
consumo_m3 = 0
custo_total = 0
ultimo_custo = 0
gasto_futuro = 0
volume_caixa = 0  # Nova variável global

@app.route('/save_data', methods=['POST'])
def save_data():
    global consumo_m3, custo_total, ultimo_custo, gasto_futuro, volume_caixa

    # Captura a data e o horário atual do sistema
    data_e_horario = datetime.now()

    # Separar os componentes da data
    dia = data_e_horario.day
    mes = data_e_horario.month
    ano = data_e_horario.year

    # Separar os componentes do horário
    hora = data_e_horario.hour
    minuto = data_e_horario.minute
    segundo = data_e_horario.second

    # Exibe os valores capturados
    print(f"\n\nDia: {dia}")
    print(f"Mês: {mes}")
    print(f"Ano: {ano}")
    print(f"Hora: {hora}")
    print(f"Minuto: {minuto}")
    print(f"Segundo: {segundo}\n")
    
    # Dados recebidos do frontend
    data = request.json
    consumo_hidrometro = data.get('consumoHidrometro')
    custo_agua = data.get('custoAgua')
    ultimo_custo_mes = data.get('ultimoCusto')
    gasto_futuro_mes = data.get('gastoFuturo')
    volume_caixa_litros = data.get('volumeCaixa')  # Nova variável recebida

    # Validação dos dados recebidos
    if any(value is None for value in [consumo_hidrometro, custo_agua, ultimo_custo_mes, gasto_futuro_mes, volume_caixa_litros]):
        return jsonify({'error': 'Dados inválidos!'}), 400

    # Atualiza as variáveis globais
    consumo_m3 = consumo_hidrometro
    custo_total = custo_agua
    ultimo_custo = ultimo_custo_mes
    gasto_futuro = gasto_futuro_mes
    volume_caixa = volume_caixa_litros

    # Log para verificar os dados recebidos
    print(f"\nConsumo registrado no mês: {consumo_hidrometro} m³")
    print(f"Custo total do mês: R$ {custo_agua}")
    print(f"Custo do último mês: R$ {ultimo_custo_mes}")
    print(f"Gasto planejado para o próximo mês: R$ {gasto_futuro_mes}")
    print(f"Volume da caixa d'água: {volume_caixa_litros} litros\n")
    
    # Função para calcular o custo por litro de água
    def calcular_custo_por_litro(consumo_m3, custo_total):
        consumo_litros = consumo_m3 * 1000  # Converte para litros
        custo_por_litro = custo_total / consumo_litros
        return custo_por_litro
    
    # Variável responsável pelo custo por litro
    custo_litro = calcular_custo_por_litro(consumo_m3, custo_total)

    # Exibindo os resultados
    print(f"\nCusto por litro de água: R$ {custo_litro:.2f} por litro\n")

    # Variáveis vindas do microocontolador 
    Q = [14, 9, 21, 17, 11, 18, 19, 22, 10, 20, 16, 13, 23, 8, 20, 15, 12, 18, 22, 14, 9, 13, 17, 11] # Em litros
    volume_caixa = 500

    # Função responsável pelo consumo na última hora
    def consumo_hora(Q, custo_litro):
        return Q * custo_litro

    consumo_ultima_hora = consumo_hora(Q[0], custo_litro)

    print(f"\nCusto na útima hora: R$ {consumo_ultima_hora:.2f}")
    print(f"Volume de água gasto na última hora: {Q[0]:.2f} litros\n")

    # Função resposável pelo consumo no dia
    Consumo_dia = [0, 387, 262, 276, 319, 369, 314, 320, 276, 345, 327, 373, 396, 347, 356, 350, 366, 388, 258, 359, 375, 381, 296, 333, 313, 366, 283, 345, 309, 328, 391] # Em litros

    for i in range(24):  
        Consumo_dia[0] += Q[i] 

    def consumo_no_dia(Consumo_dia, custo_litro):
        return Consumo_dia * custo_litro
    
    Custo_dia = consumo_no_dia(Consumo_dia[0], custo_litro)

    print(f"\nCusto da água no dia: R$ {Custo_dia:.2f}")

    print(f"Volume de agua gasto no dia: R$ {Consumo_dia[0]:.2f} litros\n\n")

    # Função responsável pelo consumo no mês
    Consumo_mes = [0, 9761, 11840, 8367, 11905, 13042, 10255, 9284, 11572, 9480, 12274, 10360] # Em litros

    for i in range(31):  
        Consumo_mes[0] += Consumo_dia[i]

    def consumo_no_mes(Consumo_mes, custo_litro):
        return Consumo_mes * custo_litro
    
    Custo_mes = consumo_no_mes(Consumo_mes[0], custo_litro)

    print(f"\nCusto da água no mês: R$ {Custo_mes:.2f}")

    print(f"Volume de agua gasto no dia: R$ {Consumo_mes[0]:.2f} litros\n")

    # Função responsável pelo consumo no ano

    Consumo_ano = [0, 0, 0, 0, 0] # Em litros

    for i in range(5):  
        Consumo_ano[0] += Consumo_mes[i]

    def consumo_no_ano(Consumo_ano, custo_litro):
        return Consumo_ano * custo_litro

    Custo_ano = consumo_no_ano(Consumo_ano[0], custo_litro)

    print(f"\nCusto da água no ano: R$ {Custo_ano:.2f}")

    print(f"Volume de agua gasto no ano: R$ {Consumo_ano[0]:.2f} litros\n")

    # Água disponível na caixa d'água

    Agua_disponivel = volume_caixa

    print(f"\nVolume de água disponível na caixa água: {Agua_disponivel:.0f} litros\n")

    # Consumo real (diferença em reais com o valor do hidrômetro)
    Difereca = ultimo_custo_mes - Custo_mes

    if Difereca < 0:
        print(f"\nO cunsumo do seu hidrometro está de acordo com o seu consumo da caixa :)\n")
    else:
        def Difereca_consumo(Difereca, ultimo_custo_mes):
            Dif = Difereca * 100
            porcentagem_dif = Dif / ultimo_custo_mes
            return porcentagem_dif
    
        P_consumo_real = Difereca_consumo(Difereca, ultimo_custo_mes)

        print(f"\nA difereça entre o consumo do hidrômetro e do equipamento é de {P_consumo_real:.2f}%")

        print(f"O que caracteriza uma difereça de R$ {Difereca:.2f}\n")

    # Caso acabe a água, tempo de água disponível na caixa d'água

    def Consumo_3_dias(Consumo_dia):
        soma_consumo = 0
        for i in range(10):  
            soma_consumo += Consumo_dia[i]
        media = soma_consumo / 10
        Tempo_agua = volume_caixa_litros / media
        return Tempo_agua

    Consumo_real_3_dias = Consumo_3_dias(Consumo_dia)

    print(f"\nDe acordo com seu consumo normal você tem água disponível para {Consumo_real_3_dias:.0f} dias\n")

    return jsonify({'message': 'Dados salvos com sucesso!'}), 200

if __name__ == '__main__':
    app.run(debug=True)

