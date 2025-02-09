from flask import Flask, request, jsonify, Response, render_template  # Adicione Response
from flask_cors import CORS
import time  # Import necessário para atrasos no envio do SSE
from datetime import datetime
import os

app = Flask(__name__, template_folder="templates")
logs = []  # Lista para armazenar mensagens de log
CORS(app)  # Ativa o CORS para o app Flask

# Variáveis globais
consumo_m3 = 0
custo_total = 0
ultimo_custo = 0
gasto_futuro = 0
volume_caixa = 0  

# Define a rota '/receive_data' que aceita apenas requisições POST
@app.route('/ESP_data', methods=['POST'])
def receive_data():
    global distancia_esp
    global logs    
    data = request.json  # Obtém os dados JSON enviados na requisição
    if not data:  # Verifica se os dados são válidos (não nulos)
        return jsonify({"error": "Dados inválidos"}), 400  # Retorna um erro 400 se os dados forem inválidos
    
    # Extrai os valores das chaves específicas no JSON recebido
    flow_rate = data.get("flow_rate")  # Vazão de água em L/min
    total_volume = data.get("total_volume")  # Volume total acumulado em litros
    distance = data.get("distance")  # Distância medida pelo sensor ultrassônico em cm
    volume_por_minuto = data.get("volume_minuto")  # Distância medida pelo sensor ultrassônico em cm
    distancia_esp = distance

    # Exibe os dados recebidos no console
    print(f"\nVazão: {flow_rate} L/min, Volume Total: {total_volume} L, Distância: {distance} cm, Volume no minuto: {volume_por_minuto} L\n")

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

    # print(f"\nAtualizado dia {dia}/{mes}/{ano} às {hora}:{minuto}:{segundo}\n")

    # Nome dos arquivos
    contador_arquivo = "contador.txt"
    valores_arquivo = "valores.txt"

    # Verifica se o arquivo do contador existe e lê o valor
    if os.path.exists(contador_arquivo):
        with open(contador_arquivo, "r") as f:
            contador = int(f.read().strip())
    else:
        contador = 0  # Se não existir, começa do zero

    # Incrementa o contador e mantém dentro do intervalo de 0 a 59 (circular)
    contador = (contador + 1) % 60

    # Salva o novo valor do contador
    with open(contador_arquivo, "w") as f:
        f.write(str(contador))

    # Verifica se o arquivo de valores existe e lê os dados antigos
    if os.path.exists(valores_arquivo):
        with open(valores_arquivo, "r") as f:
            linhas = f.readlines()
    else:
        linhas = ["0\n"] * 60  # Se não existir, inicializa com zeros

    # Atualiza a posição baseada no contador
    linhas[contador] = f"{volume_por_minuto}\n"  # Salva o novo dado na posição correta

    # Salva os valores atualizados no arquivo
    with open(valores_arquivo, "w") as f:
        f.writelines(linhas)

    # Exibe os valores salvos
    # print(f"Valor {volume_por_minuto} salvo na posição {contador + 1} do arquivo '{valores_arquivo}'\n")

    # Verifica se o arquivo existe antes de tentar ler
    if os.path.exists(valores_arquivo):
        with open(valores_arquivo, "r") as f:
            valores = [line.strip() for line in f.readlines()]  # Lê e remove quebras de linha
    else:
        valores = ["0"] * 60  # Se não existir, inicializa com zeros

    # Imprime a lista formatada
    print(f"Volume a cada minuto= {valores}\n")

    # Retorna uma resposta JSON indicando sucesso
    return jsonify({"status": "success"}), 200

@app.route('/save_data', methods=['POST'])
def save_data():
    global consumo_m3, custo_total, ultimo_custo, gasto_futuro, volume_caixa
    global logs    

    data = request.json  # Obtém os dados JSON enviados na requisição
    if not data:  # Verifica se os dados são válidos (não nulos)
        return jsonify({"error": "Dados inválidos"}), 400  # Retorna um erro 400 se os dados forem inválidos


    # logs.append(f"Atualizado dia {dia}/{mes}/{ano} às {hora}:{minuto}:{segundo}")  # Adiciona log
    logs.append(f"  ")  # Adiciona log
    
    # Dados recebidos do frontend
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
    print(f"Volume da caixa d'água: {volume_caixa_litros} litros")
    print(f"Custo do último mês: R$ {ultimo_custo_mes}")
    print(f"Gasto planejado para o próximo mês: R$ {gasto_futuro_mes}")
    print(f"Distancia balde: {distancia_esp} cm\n")

    logs.append(f"Consumo registrado no mês: {consumo_hidrometro} m³")  # Adiciona log
    logs.append(f"Custo total do mês: R$ {custo_agua}")  # Adiciona log
    logs.append(f"Volume da caixa d'água: {volume_caixa_litros} litros")  # Adiciona log
    logs.append(f"Custo do último mês: R$ {ultimo_custo_mes}")  # Adiciona log
    logs.append(f"Gasto planejado para o próximo mês: R$ {gasto_futuro_mes}")  # Adiciona log
    logs.append(f"Distancia balde: {distancia_esp} cm")
    
    # Função para calcular o custo por litro de água
    def calcular_custo_por_litro(consumo_m3, custo_total):
        consumo_litros = consumo_m3 * 1000  # Converte para litros
        custo_por_litro = custo_total / consumo_litros
        return custo_por_litro
    
    # Variável responsável pelo custo por litro
    custo_litro = calcular_custo_por_litro(consumo_m3, custo_total)

    # Exibindo os resultados
    print(f"\nCusto por litro de água: R$ {custo_litro:.2f} por litro\n")

    logs.append(f" ")  # Adiciona log
    logs.append(f"Custo por litro de água: R$ {custo_litro:.2f} por litro")  # Adiciona log

    # Variáveis vindas do microocontolador 
    Q = [14, 9, 21, 17, 11, 18, 19, 22, 10, 20, 16, 13, 23, 8, 20, 15, 12, 18, 22, 14, 9, 13, 17, 11] # Em litros
    volume_caixa = 500

    # Função responsável pelo consumo na última hora
    def consumo_hora(Q, custo_litro):
        return Q * custo_litro

    consumo_ultima_hora = consumo_hora(Q[0], custo_litro)

    logs.append(f" ")  # Adiciona log
    logs.append(f"Custo na útima hora: R$ {consumo_ultima_hora:.2f}")  # Adiciona log
    logs.append(f"Volume de água gasto na última hora: {Q[0]:.2f} litros")  # Adiciona log

    # Função resposável pelo consumo no dia
    Consumo_dia = [0, 387, 262, 276, 319, 369, 314, 320, 276, 345, 327, 373, 396, 347, 356, 350, 366, 388, 258, 359, 375, 381, 296, 333, 313, 366, 283, 345, 309, 328, 391] # Em litros

    for i in range(24):  
        Consumo_dia[0] += Q[i] 

    def consumo_no_dia(Consumo_dia, custo_litro):
        return Consumo_dia * custo_litro
    
    Custo_dia = consumo_no_dia(Consumo_dia[0], custo_litro)

    logs.append(f" ")  # Adiciona log
    logs.append(f"Custo da água no dia: R$ {Custo_dia:.2f}")  # Adiciona log
    logs.append(f"Volume de água gasto no dia: {Consumo_dia[0]:.2f} litros")  # Adiciona log

    print(f"\nCusto da água no dia: R$ {Custo_dia:.2f}")
    print(f"Volume de água gasto no dia: R$ {Consumo_dia[0]:.2f} litros\n\n")

    # Função responsável pelo consumo no mês
    Consumo_mes = [0, 9761, 11840, 8367, 11905, 13042, 10255, 9284, 11572, 9480, 12274, 10360] # Em litros

    for i in range(31):  
        Consumo_mes[0] += Consumo_dia[i]

    def consumo_no_mes(Consumo_mes, custo_litro):
        return Consumo_mes * custo_litro
    
    Custo_mes = consumo_no_mes(Consumo_mes[0], custo_litro)

    print(f"\nCusto da água no mês: R$ {Custo_mes:.2f}")

    print(f"Volume de água gasto no dia: R$ {Consumo_mes[0]:.2f} litros\n")

    logs.append(f" ")  # Adiciona log
    logs.append(f"Custo da água no mês: R$ {Custo_mes:.2f}")  # Adiciona log
    logs.append(f"Volume de água gasto no dia: {Consumo_mes[0]:.2f} litros")  # Adiciona log

    # Função responsável pelo consumo no ano

    Consumo_ano = [0, 0, 0, 0, 0] # Em litros

    for i in range(5):  
        Consumo_ano[0] += Consumo_mes[i]

    def consumo_no_ano(Consumo_ano, custo_litro):
        return Consumo_ano * custo_litro

    Custo_ano = consumo_no_ano(Consumo_ano[0], custo_litro)

    print(f"\nCusto da água no ano: R$ {Custo_ano:.2f}")

    print(f"Volume de água gasto no ano: R$ {Consumo_ano[0]:.2f} litros\n")

    logs.append(f" ")  # Adiciona log
    logs.append(f"Custo da água no ano: R$ {Custo_ano:.2f}")  # Adiciona log
    logs.append(f"Volume de água gasto no ano: R$ {Consumo_ano[0]:.2f} litros")  # Adiciona log


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

        logs.append(f" ")  # Adiciona log
        logs.append(f"A difereça entre o consumo do hidrômetro e do equipamento é de {P_consumo_real:.2f}%")  # Adiciona log
        logs.append(f"O que caracteriza uma difereça de R$ {Difereca:.2f}")  # Adiciona log

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

    logs.append(f" ")  # Adiciona log
    logs.append(f"De acordo com seu consumo normal você tem água disponível para {Consumo_real_3_dias:.0f} dias")  # Adiciona log

    return jsonify({'message': 'Dados salvos com sucesso!'}), 200


@app.route('/logs_stream')
def logs_stream():
    def generate():
        last_index = 0
        while True:
            if last_index < len(logs):
                for i in range(last_index, len(logs)):
                    yield f"data: {logs[i]}\n\n"
                    print(f"Enviando log para o frontend: {logs[i]}", flush=True)  # Debug para ver no terminal
                last_index = len(logs)
            time.sleep(1)  # Aguarda 1 segundo antes de verificar novamente
    return Response(generate(), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
