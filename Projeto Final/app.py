from flask import Flask, request, jsonify, Response, render_template  # Adicione Response
from flask_cors import CORS
import time  # Import necessário para atrasos no envio do SSE
from datetime import datetime
import os
import json

app = Flask(__name__, template_folder="templates")
logs = []  # Lista para armazenar mensagens de log
CORS(app)  # Ativa o CORS para o app Flask

# Define a rota '/receive_data' que aceita apenas requisições POST
@app.route('/ESP_data', methods=['POST'])
def receive_data():

    global logs    #Variável de envio para frontend

    data = request.json  # Obtém os dados JSON enviados na requisição

    if not data:  # Verifica se os dados são válidos (não nulos)
        return jsonify({"error": "Dados inválidos"}), 400  # Retorna um erro 400 se os dados forem inválidos
    
    # Variáveis vindas da ESP
    distance = data.get("distance")  # Distância medida pelo sensor ultrassônico em cm
    volume_por_minuto = data.get("volume_minuto")  # Volume de água total no último minuto
    flow_rate = data.get("flow_rate")  # Vazão de água em L/min
    total_volume = data.get("total_volume")  # Volume total acumulado em litros
    falta_agua = data.get("falta_agua") # Exibe o valor de 1 para indicação de falta de água
    

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

    # Arquivos .txt
    contador_arquivo = "contador.txt" # Arquiva o valor do contador
    valores_arquivo = "valores.txt" # Arquiva os valores de volume por minuto e volume por hora

    ## -- contador.txt -- ##

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

    ## -- -- ##

    ## -- valores.txt -- ##

    # Verifica se o arquivo de valores existe e lê os dados antigos
    if os.path.exists(valores_arquivo):
        with open(valores_arquivo, "r") as f:
            linhas = f.readlines()
    else:
        # Se o arquivo não existir, cria listas vazias
        linhas = ["0\n"] * 60 + ["0\n"] * 24

    # Atualiza a posição baseada no contador
    linhas[contador] = f"{volume_por_minuto}\n"  # Salva o novo dado na posição correta

    # Quando o contador atinge 59, atualiza a lista de 24 valores
    if contador == 59:
        # Obtém os 60 valores e soma
        valores_60 = [float(linhas[i].strip()) for i in range(60)]
        soma = sum(valores_60)

        # Certifica-se de que 'linhas' tem pelo menos 84 elementos
        while len(linhas) < 84:
            linhas.append("0\n")  # Preenche com zeros caso faltem linhas

        # Lê a lista de 24 somas anteriores
        lista_24 = [float(linhas[i + 60].strip()) for i in range(24)]

        # Insere a nova soma na posição correta, deslocando os valores anteriores
        lista_24.pop(0)  # Remove o primeiro valor para manter sempre 24 elementos
        lista_24.append(soma)  # Adiciona a nova soma ao final

        # Atualiza a parte do arquivo correspondente à lista de 24 valores
        for i in range(24):
            linhas[i + 60] = f"{lista_24[i]}\n"

    # Salva os valores atualizados no arquivo
    with open(valores_arquivo, "w") as f:
        f.writelines(linhas)

    # -- -- ##

    # Certifica-se de que 'linhas' tenha pelo menos 60 elementos antes de acessar
    while len(linhas) < 60:
        linhas.append("0\n")

    # Obtém a lista de volume por minuto
    valores_60 = [float(linhas[i].strip()) for i in range(60)]

    # Imprime a lista de volume por minuto
    print(f"\nVolume a cada minuto= {valores_60}\n")

    # Obtém a lista de volume por hora
    lista_24 = [float(linhas[i + 60].strip()) for i in range(24)]

    # Imprime a lista de volume por hora
    print(f"Lista a cada hora= {lista_24}\n")

    ## -- implementação do cadastro inicial vindo do frontend -- ##

    # Nome do arquivo onde os dados estão armazenados
    dados_arquivo = "dados.txt"

    # Faz a leitura dos dados do cadastro inicial
    def carregar_dados():
        """Lê os dados do arquivo e retorna como um dicionário."""
        try:
            with open(dados_arquivo, "r") as f:
                dados = json.load(f)  # Converte JSON para dicionário Python
            return dados
        except (FileNotFoundError, json.JSONDecodeError):
            print("Erro ao ler o arquivo. Verifique se ele existe e está formatado corretamente.")
            return None  # Retorna None se houver erro
        
    # Carregar os dados
    dados = carregar_dados()

    # Aloca aos dados em variáveis
    if dados:
        consumo_hidrometro = dados["consumo_hidrometro"]
        custo_agua = dados["custo_agua"]
        ultimo_custo_mes = dados["ultimo_custo_mes"]
        gasto_futuro_mes = dados["gasto_futuro_mes"]
        volume_caixa_litros = dados["volume_caixa_litros"]

    # Função para calcular o custo por litro de água
    def calcular_custo_por_litro(consumo_hidrometro, custo_agua):
        consumo_litros = consumo_hidrometro * 1000  # Converte para litros
        custo_por_litro = custo_agua / consumo_litros
        return custo_por_litro
    
    # Variável responsável pelo custo por litro
    custo_litro = calcular_custo_por_litro(consumo_hidrometro, custo_agua)

    # Imprime no terminal e no frontend o valor por litro da água 
    print(f"Custo por litro de água: R$ {custo_litro:.2f} por litro\n")

    # Curto por minuto
    Custo_60 = [valor * custo_litro for valor in valores_60]

    # Curto por hora
    Custo_24 = [valor * custo_litro for valor in lista_24]

    # Função responsável pelo consumo no útimo minuto 
    def consumo_minuto(valores_60, custo_litro):
        return valores_60 * custo_litro
    
    # Consumo no útimo minuto registrado pelo sensor
    consumo_ultimo_minuto = consumo_minuto(valores_60[contador], custo_litro)

    # Imprime no terminal o comsumo no último minuto em reais e litros
    print(f"Custo na último minuto: R$ {consumo_ultimo_minuto:.2f}")
    print(f"Volume de água gasto na último minuto: {valores_60[contador]:.2f} litros\n")

    # Função responsável pelo consumo em reais para cada hora
    def consumo_hora(lista_24, custo_litro):
        return lista_24 * custo_litro
    
    # Consumo na última hora registrado pelo sensor
    consumo_ultimo_hora = consumo_hora(lista_24[23], custo_litro)

    # Imprime no terminal o comsumo na última hora
    # print(f"Custo na última hora: R$ {consumo_ultimo_hora:.2f}")
    # print(f"Consumo de água na última hora: {lista_24[23]:.2f} litros\n")

    # Calcula o total de água gasta nas últimas 24 horas
    soma_dia = sum(lista_24[:24])

    # Gasto de água em reais das últimas 24 horas 
    consumo_dia = soma_dia * custo_litro

    # Envia os dados para o frontend do card "Seu consumo"
    logs.append(json.dumps({"valores_60": valores_60, "lista_24": lista_24, "soma_dia": soma_dia, "Custo_60": Custo_60, "Custo_24": Custo_24, "consumo_dia": consumo_dia}))

    # Imprime no terminal o comsumo nas últimas 24 horas
    # print(f"Custo nas últimas 24 horas: R$ {consumo_dia:.2f}")
    # print(f"Consumo de água nas últimas 24 horas: {soma_dia} litros\n")

    ## -- Volume de água disponível -- ##
    if distance <= 5:
        Volume_atual = volume_caixa_litros
        print(f"Caixa d'água cheia! {Volume_atual:.2f} Litros")

    elif distance >= 19.6:
        Volume_atual = 0
        print(f"Caixa d'água vazia! {Volume_atual:.2f} Litros")

    elif 5 < distance < 19.6:
        Volume_atual = (20 - distance) / 3  # A cada 3 cm, 1 litro a mais
        print(f"Volume de água na caixa d'água: {Volume_atual:.2f} Litros")
   
    def Consumo_60_minutos(lista_24): # Caso a água acabe, quanto tempo de água disponível teremos na caixa d'água
        media_consumo = 0
        media_consumo = soma_dia / (60*24)
        Tempo_agua = Volume_atual / media_consumo
        return Tempo_agua

    Consumo_esperado = Consumo_60_minutos(lista_24)

    print(f"\nDe acordo com seu consumo normal você tem água disponível para {Consumo_esperado:.2f} minutos\n")

    ## -- -- ##

    # Detecção de falta d'água
    if (falta_agua == 1):
        print("ALERTA: Falta de água detectada!")


    ## -- Diferença em relação ao hidrometro -- ##

    Difereca = ultimo_custo_mes - (lista_24[23]*custo_litro)

    def Difereca_consumo(Difereca, ultimo_custo_mes):
        if ultimo_custo_mes == 0:  # Evita divisão por zero
            return 0
        Dif = Difereca * 100
        porcentagem_dif = Dif / ultimo_custo_mes
        return porcentagem_dif

    if Difereca < 0:
        print(f"\nO consumo do seu hidrômetro está de acordo com o seu consumo da caixa :)\n")
        P_consumo_real = 0  # Agora a variável recebe o valor corretamente
        Difereca = 0  # Ajusta Difereca para que a mensagem final faça sentido
    else:
        P_consumo_real = Difereca_consumo(Difereca, ultimo_custo_mes)
        print(f"\nA diferença entre o consumo do hidrômetro e do equipamento é de {P_consumo_real:.2f}%")
        print(f"O que caracteriza uma diferença de R$ {Difereca:.2f}\n")

    ## -- -- ##

    ## -- Cálculo para gasto futuro -- ##

    def Consumo_3_horas(lista_24, custo_litro):
        if len(lista_24) < 3:
            return 0  # Evita erro caso a lista tenha menos de 3 elementos
        media_consumo = sum(x * custo_litro for x in lista_24[-3:]) / 3  # Multiplica cada elemento antes de calcular a média
        return media_consumo

    Consumo_media_3_horas = Consumo_3_horas(lista_24, custo_litro)

    Diferenca_futuro = Consumo_media_3_horas - gasto_futuro_mes

    def Diferenca_consumo_futuro(Diferenca_futuro, Consumo_media_3_horas):
        if Consumo_media_3_horas == 0:  # Evita divisão por zero
            return 0  # Retorna zero ao invés de uma string

        porcentagem_dif = (Diferenca_futuro * 100) / Consumo_media_3_horas
        return porcentagem_dif  # Retorna apenas o valor numérico

    porcentagem_diferenca = Diferenca_consumo_futuro(Diferenca_futuro, Consumo_media_3_horas)

    if porcentagem_diferenca <= 0:
        print("O seu consumo normal está de acordo com a sua expectativa.")
    else:
        print(f"A diferença percentual no consumo futuro é de {porcentagem_diferenca:.2f}%")

    ## -- -- ##

    # Envia os dados para o frontend do card "Painel"
    logs.append(json.dumps({
        "falta_agua": falta_agua,  # Garante que seja um número
        "Volume_atual": round(Volume_atual, 1),
        "Consumo_esperado": round(Consumo_esperado, 1),
        "Difereca": round(Difereca, 2),
        "P_consumo_real": round(P_consumo_real, 0),
        "porcentagem_diferenca": round(porcentagem_diferenca, 0)
    }))

    # Retorna uma resposta JSON indicando sucesso
    return jsonify({"status": "success"}), 200

@app.route('/save_data', methods=['POST'])
def save_data():

    global logs # Variável de envio para frontend

    data = request.json  # Obtém os dados JSON enviados na requisição
    if not data:  # Verifica se os dados são válidos (não nulos)
        return jsonify({"error": "Dados inválidos"}), 400  # Retorna um erro 400 se os dados forem inválidos

    # Dados recebidos do frontend
    consumo_hidrometro = data.get('consumoHidrometro')
    custo_agua = data.get('custoAgua')
    ultimo_custo_mes = data.get('ultimoCusto')
    gasto_futuro_mes = data.get('gastoFuturo')
    volume_caixa_litros = data.get('volumeCaixa')  # Nova variável recebida

    # Validação dos dados recebidos #
    
    if any(value is None for value in [consumo_hidrometro, custo_agua, ultimo_custo_mes, gasto_futuro_mes, volume_caixa_litros]):
        return jsonify({'error': 'Dados inválidos!'}), 400

    ## -- dados.txt -- ##

    # Nome do arquivo onde os dados serão armazenados
    dados_arquivo = "dados.txt"

    # Dados padrão caso o arquivo ainda não exista
    dados_padrao = {
        "consumo_hidrometro": 0.0,
        "custo_agua": 0.0,
        "ultimo_custo_mes": 0.0,
        "gasto_futuro_mes": 0.0,
        "volume_caixa_litros": 0
    }

    # Verifica se o arquivo existe, se não existir, cria com valores padrão
    if not os.path.exists(dados_arquivo):
        with open(dados_arquivo, "w") as f:
            json.dump(dados_padrao, f, indent=4)
        print(f"Arquivo '{dados_arquivo}' criado com valores padrão.")

    # Agora, sempre que rodar o código, ele substituirá os valores no arquivo
    dados_novos = {
        "consumo_hidrometro": consumo_hidrometro,  # Exemplo de valor, substitua pelo valor real
        "custo_agua": custo_agua,
        "ultimo_custo_mes": ultimo_custo_mes,
        "gasto_futuro_mes": gasto_futuro_mes,
        "volume_caixa_litros": volume_caixa_litros
    }

    # Salva os novos dados no arquivo, sobrescrevendo os valores anteriores
    with open(dados_arquivo, "w") as f:
        json.dump(dados_novos, f, indent=4)

    ## -- -- ##
    
    # Imprimir no terminal os dados recebidos do frontend
    print(f"\nConsumo registrado no mês: {consumo_hidrometro} m³")
    print(f"Custo total do mês: R$ {custo_agua}")
    print(f"Volume da caixa d'água: {volume_caixa_litros} litros")
    print(f"Custo do último mês: R$ {ultimo_custo_mes}")
    print(f"Gasto planejado para o próximo mês: R$ {gasto_futuro_mes}")

    return jsonify({'message': 'Dados salvos com sucesso!'}), 200

## -- Configuração do envio de informações para o frontend -- ##

@app.route('/logs_stream')
def logs_stream():
    def generate():
        last_index = 0
        while True:
            if last_index < len(logs):
                for i in range(last_index, len(logs)):
                    yield f"data: {logs[i]}\n\n"
                    # print(f"Enviando log para o frontend: {logs[i]}", flush=True)  # Debug para ver no terminal
                last_index = len(logs)
            time.sleep(1)  # Aguarda 1 segundo antes de verificar novamente
    return Response(generate(), content_type='text/event-stream')

## -- -- ##

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
