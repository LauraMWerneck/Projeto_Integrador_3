# Desenvolvimento de Firmware para Comunicação com o Sensor

Esta etapa consiste no teste do firmware para a comunicação entre o sensor de fluxo de água YF-S201 e o microcontrolador 
ESP32, medindo a vazão de água. Para isso, implementamos um firmware que permitiu a leitura e o processamento dos 
dados de vazão fornecidos pelo sensor YF-S201, estabelecendo comunicação eficiente e confiável com a ESP32.

## Descrição do Funcionamento

Para medir a vazão de água, o sensor YF-S201 gera pulsos que são capturados pelo pino GPIO da ESP32. Cada pulso corresponde 
a uma quantidade específica de água que passa pelo sensor, definida por sua constante `PULSOS_POR_LITRO`. Este valor é 
utilizado no cálculo da vazão em litros por minuto (L/min).

### Pinos da ESP32

A ESP32 é uma placa muito popular para projetos de IoT e eletrônica. Ela vem com Wi-Fi e Bluetooth integrados, 
além de vários pinos de entrada e saída (GPIOs), que permitem conectar diferentes sensores e dispositivos. 
Cada pino tem funções específicas, como comunicação e controle. Na Figura 1 é mostrado o pinout da ESP32, 
mostrando a disposição dos pinos e suas funções:

**Figura 1:** Pinos ESP32.

![Pinos ESP32](https://i0.wp.com/circuits4you.com/wp-content/uploads/2018/12/ESP32-Pinout.jpg?w=758&ssl=1)

Fonte: [CIRCUITS4YOU](https://circuits4you.com/2018/12/31/esp32-devkit-esp32-wroom-gpio-pinout/).

### Configurações do Sensor

- **Pino de Sinal**: GPIO4 da ESP32
- **Pulsos por Litro**: 450 (configuração específica para o sensor YF-S201)

## Código de Teste

Abaixo está o código de teste utilizado para configurar o pino do sensor, definir a interrupção para contar os pulsos e 
calcular a vazão de água:

```c
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_timer.h"

#define YFS201_PIN GPIO_NUM_4   // Pino GPIO que o pino de sinal do sensor é conectado
#define PULSOS_POR_LITRO 450    // Pulsos por litro para do sensor YF-S201

volatile uint32_t contador_pulsos = 0;  // Contador de pulsos do sensor

// Função da interrupção, que é chamada a cada pulso do sensor
static void IRAM_ATTR contar_pulsos(void* arg) {
    contador_pulsos++;
}

// Função para configurar o GPIO e a interrupção
void setup_gpio() {
    gpio_config_t io_conf = {
        .intr_type = GPIO_INTR_POSEDGE,      // Interrupção na borda de subida
        .mode = GPIO_MODE_INPUT,             // Configura o pino como entrada
        .pin_bit_mask = (1ULL << YFS201_PIN) // Define o pino do sensor
    };
    gpio_config(&io_conf);                   // Aplica as configurações
    gpio_install_isr_service(0);             // Inicia o serviço de interrupção
    gpio_isr_handler_add(YFS201_PIN, contar_pulsos, NULL); // Adiciona a interrupção
}

// Função principal para medir a vazão de água
void medir_vazao() {
    uint32_t pulso_inicial = 0;
    float vazao_litros_por_minuto = 0;

    // Intervalo de tempo em segundos para calcular a vazão 
    const float intervalo_segundos = 1.0;
    
    while (1) {
        // Salva o contador de pulsos e zera para próxima medição
        pulso_inicial = contador_pulsos;
        contador_pulsos = 0;
        
        // Aguarda o intervalo de tempo especificado
        vTaskDelay((int)(intervalo_segundos * 1000) / portTICK_PERIOD_MS);
        
        // Calcula a vazão em litros por minuto 
        vazao_litros_por_minuto = (pulso_inicial / intervalo_segundos) * (60.0 / PULSOS_POR_LITRO);

        // Exibe o resultado
        printf("Vazão: %.2f L/min\n", vazao_litros_por_minuto);
    }
}

void app_main() {
    setup_gpio();           // Configura o pino GPIO e a interrupção
    medir_vazao();          // Inicia a medição da vazão de água
}
```

## Explicação do Código

1. **Configuração do Pino GPIO**: O pino GPIO4 é configurado como entrada para receber os pulsos do sensor.
Configuramos uma interrupção para que, a cada pulso detectado (borda de subida), a função `contar_pulsos` incremente o
contador de pulsos.

4. **Interrupção de Pulso**: A função `contar_pulsos` é chamada a cada pulso, registrando a passagem da água pelo sensor.

5. **Cálculo da Vazão**: A função `medir_vazao` calcula a vazão de água em litros por minuto com base na quantidade de
pulsos contados em um intervalo específico.

## Resultados

Ao executar este código, o sistema apresenta a vazão de água em litros por minuto no terminal do ESP32, permitindo o monitoramento 
em tempo real da quantidade de água que passa pelo sensor. Para realizar esse teste inicial, utilizamos o vento para ativar a 
ventoinha, assoprando pela abertura do sensor em vez testando com água. A Figura 2 ilustra a conexão do sensor ao ESP, enquanto
a Figura 3 exibe o resultado no monitor serial ao executar o script.

**Figura 2:** Ligação do sensor na ESP.

![Ligação do sensor na ESP](https://github.com/LauraMWerneck/Projeto_Integrador_3/blob/main/Etapa%202/Sensor%20de%20Vaz%C3%A3o/Teste%20de%20Firmware/conexao_esp_yfs201.jpg)

Fonte: Autoria própria.

**Figura 3:** Saida monitor serial.

![Saida monitor serial](https://github.com/LauraMWerneck/Projeto_Integrador_3/blob/main/Etapa%202/Sensor%20de%20Vaz%C3%A3o/Teste%20de%20Firmware/monitor_serial.png)

Fonte: Autoria própria.

## Referências

CIRCUITS4YOU. *ESP32 DevKit ESP32 Wroom GPIO Pinout*. Disponível em: https://circuits4you.com/2018/12/31/esp32-devkit-esp32-wroom-gpio-pinout/. Acesso em: 4 nov. 2024.
