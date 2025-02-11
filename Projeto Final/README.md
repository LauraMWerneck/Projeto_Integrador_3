# Explicação dos códigos

# [main.c](https://github.com/LauraMWerneck/Projeto_Integrador_3/blob/main/Projeto%20Final/main.c)

O código main.c é responsável pelo monitoramento do fluxo de água e do nível de um reservatório utilizando um ESP32. Ele coleta dados 
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

# [app.py](

