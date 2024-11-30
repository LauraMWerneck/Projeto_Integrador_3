# Integração dos Sensores

Nesta etapa, foi realizada a integração de todos os sensores, incluindo o sensor de vazão (YF-S201) e o sensor de volume (HC-SR04).
Para isso, foi desenvolvido um código que combina o controle de vazão, previamente testado, com o cálculo de distância do sensor de volume.

## Documentação do Código

O código pode ser acessado através deste [link](https://github.com/LauraMWerneck/Projeto_Integrador_3/blob/main/Etapa%203/Integra%C3%A7%C3%A3o%20dos%20Sensores/integracao_sensores.c).

### Dependências/Bibliotecas Incluídas:
- `<stdio.h>`: Para funções de entrada e saída, como `printf`.
- `<stdint.h>`: Para tipos de dados de largura fixa, como `uint32_t`.
- `<stdbool.h>`: Para uso do tipo `bool`.
- `freertos/FreeRTOS.h` e `freertos/task.h`: Para utilização do FreeRTOS, permitindo multitarefa.
- `driver/gpio.h`: Para manipulação dos pinos GPIO do ESP32.
- `esp_timer.h`: Para operações relacionadas a temporização.
- `esp_task_wdt.h`: Para o watchdog timer, garantindo que tarefas longas sejam monitoradas.

### Constantes
- `ULTRASONIC_TRIG_PIN` e `ULTRASONIC_ECHO_PIN`: Definem os pinos GPIO usados pelo sensor ultrassônico.
- `YFS201_PIN`: Pino GPIO usado pelo sensor de vazão YF-S201.
- `TIMEOUT_US`: Define o tempo máximo para medir distância pelo sensor ultrassônico.
- `PULSOS_POR_LITRO`: Especifica o número de pulsos gerados pelo sensor YF-S201 por litro de água.

### Variáveis Globais
- `contador_pulsos`: Variável volátil que registra o número de pulsos detectados pelo sensor de vazão.
- `ultrasonicTaskHandle` e `flowTaskHandle`: Handles para gerenciar as tarefas do FreeRTOS.

### Funções

`contar_pulsos(void* arg)`: Função de interrupção associada ao sensor YF-S201. Ela incrementa o contador de pulsos a cada sinal detectado.

`init_ultrasonic_sensor()`: Configura os pinos GPIO para o sensor ultrassônico: TRIG como saída e ECHO como entrada.

`measure_distance()`: Realiza a medição da distância usando o sensor ultrassônico. Isso é feito gerando um pulso de 10 µs 
no pino TRIG. Após isso espera o início do pulso de retorno no pino ECHO. Com isso, mede o tempo de subida e descida do pulso
e calcula a distância. A função retorna a distância medida ou -1 em caso de timeout.
  
`ultrasonic_task(void *pvParameters)`: Responsável por medir e exibir a distância continuamente. Ela inicializa o sensor ultrassônico, 
mede a distância a cada 1 segundo e exibe a distância no terminal.

`setup_yfs201_gpio()`: Configura o GPIO do sensor de vazão YF-S201: define o pino como entrada e configura a interrupção para 
detectar pulsos.
  
`flow_task(void *pvParameters)`: Responsável por medir a vazão de água e o volume acumulado. Configura o GPIO do sensor de vazão e 
calcula a vazão e o volume em intervalos de 1 segundo. Após o cálculo exibe os resultados no terminal.

`supervisor_task(void *pvParameters)`: Gerencia a criação e execução das tarefas dos sensores. Ela cria as tarefas `ultrasonic_task` 
e `flow_task`. Além disso exibe mensagens de supervisão a cada 2 segundos.

`app_main()`: Função principal executada ao iniciar o microcontrolador. Ela cria a tarefa de supervisão com prioridade máxima.

### Fluxo do Programa
1. **Inicialização**:
   - Configuração dos pinos GPIO para os sensores.
   - Registro da função de interrupção para o sensor de vazão.
2. **Execução das Tarefas**:
   - **`ultrasonic_task`**: Mede e exibe a distância usando o sensor ultrassônico.
   - **`flow_task`**: Calcula e exibe a vazão e o volume total de água.
   - **`supervisor_task`**: Supervisiona a execução das outras tarefas.
3. **Resultados**:
   - Distância medida pelo sensor ultrassônico.
   - Vazão em litros por minuto.
   - Volume acumulado em litros.

### Saída
Durante a execução, o programa exibe no terminal:
- **Distância (cm)**: Medida pelo sensor ultrassônico.
- **Vazão (L/min)**: Taxa de fluxo de água calculada pelo sensor de vazão.
- **Volume Total (L)**: Volume acumulado de água.
