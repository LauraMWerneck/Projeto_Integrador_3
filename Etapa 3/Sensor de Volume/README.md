# Teste Individual do Sensor de Volume Ultrassônico

Este teste avaliou o funcionamento de um sistema baseado no sensor ultrassônico **HC-SR04** para medições de distância. O objetivo foi validar a precisão do sensor e sua aplicação em cálculos de volume de água, integrando dados de distância e vazão.

## Documentação do Código

O código pode ser acessado através deste [link](https://github.com/StanisLK/Projeto_Integrador_3/blob/main/Etapa%203/Sensor%20de%20Volume/Sensor%20volume.c).

### Dependências e Bibliotecas Utilizadas

- **Ultrassônico:**
  - `<stdio.h>`: Entrada e saída.
  - `<stdint.h>`: Tipos de dados.
  - `<stdbool.h>`: Controle booleano.
  - `freertos/FreeRTOS.h`: Multitarefa.
  - `driver/gpio.h`: Manipulação de pinos GPIO.
  - `esp_timer.h`: Temporização.
  - `esp_task_wdt.h`: Watchdog Timer.

### Configurações do Sensor

- **Sensor Ultrassônico:**
  - `TRIG_PIN`: GPIO conectado ao pino TRIG.
  - `ECHO_PIN`: GPIO conectado ao pino ECHO.
  - `TIMEOUT_US`: Tempo limite para medição ultrassônica (25 ms).

### Funções Principais

#### Sensor Ultrassônico
1. **`init_ultrasonic_sensor`**: Configura os pinos TRIG e ECHO.
2. **`measure_distance`**: Mede a distância com base no tempo do sinal de eco.
3. **`ultrasonic_task`**: Executa medições contínuas e ajusta o ponto de referência quando necessário.

#### Comunicação UART
1. **`uart_task`**: Monitora a entrada serial para comandos, como ajuste do ponto de referência do sensor ultrassônico.

#### Fluxo Geral
1. Configuração e inicialização do sensor.
2. Execução simultânea das medições de distância e vazão.
3. Comunicação serial para ajustes e monitoramento.

### Saída
Durante a execução, o programa exibe no terminal:
- Vazão em Litros por Minuto (L/min).
- Distância em centímetros (cm).

## Resultados Obtidos com o Teste

### Etapas do Teste
1. O sensor foi configurado para ajustar dinamicamente a base de medição, utilizando o nível mínimo de água como referência.
2. Adicionou-se 1 litro de água em um balde, verificando a medição do nível de água com o sensor e comparando-a com uma trena.

### Dados Coletados
Após adicionar de 0 a 5 litros de água no balde, foram registrados os seguintes valores de nível medido (em cm):

| Volume (L) | Nível Medido (cm) |
|------------|-------------------|
| 0          | 0.00             |
| 1          | 3.96             |
| 2          | 7.22             |
| 3          | 10.88            |
| 4          | 13.92            |
| 5          | 16.47            |

### Curva de Nível x Volume

A curva gerada demonstra que a relação entre o nível medido e o volume não é linear, devido ao formato do recipiente utilizado, conforme imagem a seguir. O gráfico e sua análise indicam a possibilidade de criar uma função de mapeamento para estimar automaticamente o volume de água em diferentes tipos de recipientes, sem necessidade de especificação manual de dimensões.
![Curva de Volume x Nível](https://github.com/user-attachments/assets/ceabdf0f-8650-4420-b5b2-59a1d5671539)

  <img src="https://github.com/user-attachments/assets/b0d0b7fe-fad6-4606-b0c3-3901f37c0081" alt="Configuração do Sistema" width="500">


### Imagens do Teste

<p align="center">
  <img src="https://github.com/user-attachments/assets/3f2631f4-868f-4f76-91e0-6d6e416e69b6" alt="Medição com Trena" width="500">
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/0af5d7fc-459a-4e86-a77d-d63b5a6f6f59" alt="Sensor em Operação" width="500">
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/9273fed1-1778-41f9-9501-68d4403d586e" alt="IMG_6714" width="500">
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/3322c206-6ac6-400a-8643-1f0fc3956879" alt="IMG_6715" width="500">
</p>

### Conclusão
Este teste reforça a aplicabilidade do sensor ultrassônico na medição dinâmica de volumes de água, sendo uma abordagem viável e suficientemente precisa para a aplicação neste projeto.
