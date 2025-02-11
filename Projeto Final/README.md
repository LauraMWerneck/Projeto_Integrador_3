# Explicação dos códigos

# [main.c](https://github.com/LauraMWerneck/Projeto_Integrador_3/blob/main/Projeto%20Final/main.c)

O código `main.c` é responsável pelo monitoramento do fluxo de água e do nível de um reservatório utilizando um ESP32. Ele coleta dados 
dos sensores de fluxo e ultrassônico, controla um relé com base nos níveis detectados e envia as informações para um servidor remoto via 
HTTP POST. Além disso, o código gerencia a conexão Wi-Fi, garantindo que o ESP32 esteja sempre conectado para transmitir os dados coletados.

## Funcionalidades
- **Monitoramento do fluxo de água**: Mede a vazão em litros por minuto.
- **Monitoramento do nível de água**: Mede a distância entre o sensor e a superfície da água.
- **Controle de relé**: Ativa ou desativa o relé com base na distância medida pelo sensor ultrassônico.
- **Envio de dados via HTTP POST**: Envia informações para um servidor remoto.

## Coleta de Dados
A coleta de dados ocorre a cada segundo e envolve:
1. **Sensor de Fluxo YF-S201**:
   - O sensor gera pulsos conforme a passagem da água.
   - O ESP32 conta esses pulsos usando uma interrupção no pino `GPIO_NUM_4`.
   - A vazão em litros por minuto é calculada com base nos pulsos.

2. **Sensor Ultrassônico HC-SR04**:
   - Envia um pulso de 10µs pelo pino `TRIG` (`GPIO_NUM_19`).
   - Mede o tempo de resposta do pino `ECHO` (`GPIO_NUM_18`).
   - A distância é calculada a partir do tempo do eco.

3. **Controle do Relé**:
   - Se a distância medida for menor ou igual a 5cm, o relé é ativado (`GPIO_NUM_23`).
   - Se não houver fluxo de água, um alerta de falta de água é ativado.

## Conexão Wi-Fi
O ESP32 se conecta a uma rede Wi-Fi para envio de dados. O processo envolve:
1. **Inicialização do NVS (Non-Volatile Storage)** para armazenar credenciais.
2. **Criação da interface Wi-Fi no modo STA (estação)**.
3. **Configuração das credenciais Wi-Fi**:
   ```c
   #define WIFI_SSID "NomeDaRede"
   #define WIFI_PASS "SenhaDaRede"
   ```
4. **Conexão automática** com a rede configurada.
5. **Monitoramento da conexão** para reconectar em caso de falha.

## Envio de Dados
Os dados coletados são enviados para um servidor HTTP configurado na seguinte URL:
```c
#define SERVER_URL "http://192.168.0.103:5000/ESP_data"
```

O envio ocorre a cada 60 segundos e segue estes passos:
1. Os dados são formatados em um JSON:
   ```c
   snprintf(payload, sizeof(payload), 
   "{\"flow_rate\":%.2f,\"total_volume\":%.2f,\"distance\":%.2f,\"volume_minuto\":%.2f, \"falta_agua\":%d}",
   vazao, volume_total, distancia, volume_por_minuto, falta_agua);
   ```
2. O ESP32 realiza uma requisição HTTP POST com o JSON.
3. O servidor responde confirmando o recebimento.
4. Em caso de falha, o erro é registrado nos logs para depuração.

## Estrutura do Código
1. **Configuração dos pinos** para sensores e relé.
2. **Configuração do Wi-Fi** para conexão com a rede.
3. **Função de medição de distância** com o sensor ultrassônico.
4. **Função de contagem de pulsos** do sensor de fluxo.
5. **Monitoramento em loop**:
   - Mede vazão e volume de água.
   - Mede a distância do nível de água.
   - Controla o relé com base no nível.
   - Envia dados para o servidor a cada minuto.

## Logs e Depuração
O ESP32 exibirá logs via serial, como por exemplo:
```sh
Vazão: 1.25 L/min, Volume Total: 2.50 L, Distância: 10.2 cm, Falta água: 0
```
Caso haja falha no envio HTTP, uma mensagem de erro será exibida.

# [app.py](https://github.com/LauraMWerneck/Projeto_Integrador_3/blob/main/Projeto%20Final/app.py)

O código `app.py` é responsável por criar e configurar uma API web utilizando o framework Flask. Essa API é projetada para se comunicar com um sistema de monitoramento de consumo de água e controle de caixa d'água, permitindo tanto o envio de dados do sensor quanto o recebimento e armazenamento de configurações de consumo de água. A aplicação também realiza cálculos relacionados ao consumo, como o custo da água, tempo estimado de consumo, e alertas de falta d'água, além de fornecer esses dados para um painel de visualização em tempo real no frontend.

## Funcionalidades

1. **Recepção de Dados de Sensores (`/ESP_data`)**  
   A rota `/ESP_data` recebe dados de sensores (como distância, volume de água consumido, e taxa de vazão), realiza o processamento e armazena essas informações em arquivos. Além disso, calcula o consumo de água em reais, faz a comparação entre o consumo registrado e o hidrometro, calcula o tempo estimado de água disponível na caixa d'água e gera alertas caso a falta de água seja detectada.

2. **Cadastro de Configurações do Sistema (`/save_data`)**  
   A rota `/save_data` permite o envio de configurações para o sistema, como consumo do hidrômetro, custo da água, e o volume da caixa d'água. Esses dados são armazenados em um arquivo JSON chamado `dados.txt`.

3. **Stream de Logs para o Frontend (`/logs_stream`)**  
   A aplicação utiliza Server-Sent Events (SSE) para enviar logs em tempo real para o frontend, permitindo a atualização constante dos dados sem a necessidade de reatualizar a página.

4. **Leitura de Dados de Arquivo (`dados.txt`)**  
   O sistema realiza a leitura do arquivo `dados.txt` para obter os valores de consumo, custo e volume da caixa d'água. Se o arquivo não existir, ele será criado com valores padrão.

## Estrutura de Arquivos

- **`dados.txt`**: Armazena as configurações do sistema, como consumo do hidrômetro, custo da água, volume da caixa d'água, e outros dados relevantes.
- **`contador.txt`**: Mantém o valor do contador para garantir o controle dos dados mensais.
- **`valores.txt`**: Armazena os valores do volume de água consumido por minuto e por hora.
- **`logs`**: Armazena logs gerados pela aplicação que são enviados ao frontend via SSE.

## Endpoints

- **`POST /ESP_data`**: Envia dados do sensor (distância, volume, vazão).
- **`POST /save_data`**: Envia configurações do sistema (consumo do hidrômetro, custo da água, etc.).
- **`GET /logs_stream`**: Recupera os logs em tempo real via SSE.

## Dados Esperados

- Para a rota `/ESP_data`:
  - **Exemplo de dados**:
    ```json
    {
      "distance": 10.5,
      "volume_minuto": 1.25,
      "flow_rate": 0.5,
      "total_volume": 100,
      "falta_agua": 0
    }
    ```

- Para a rota `/save_data`:
  - **Exemplo de dados**:
    ```json
    {
      "consumoHidrometro": 5.2,
      "custoAgua": 15.5,
      "ultimoCusto": 10.25,
      "gastoFuturo": 18.0,
      "volumeCaixa": 500
    }
    ```

## Cálculos Realizados

1. **Cálculo de Custo por Litro de Água**  
   O custo por litro de água é calculado dividindo o custo total da água pelo consumo registrado no hidrômetro.

2. **Cálculo de Consumo por Minuto e Hora**  
   O consumo de água é registrado por minuto e por hora, com a conversão para o custo correspondente em reais.

3. **Detecção de Falta de Água**  
   Caso a distância medida seja muito baixa (indicando que a caixa d'água está vazia), o sistema gera um alerta de falta de água.

4. **Estimativa de Tempo de Água Disponível**  
   A partir da medição de volume na caixa d'água e da média de consumo diário, é calculado quanto tempo o restante da água disponível será suficiente.

