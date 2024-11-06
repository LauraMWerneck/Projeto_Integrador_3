# Sensor de Volume (Nível) com Sensor Ultrassônico HC-SR04

Este projeto implementa a medição de distância utilizando o sensor ultrassônico HC-SR04 em um ESP32, através do ESP-IDF no Visual Studio Code.

## Requisitos

- [ESP-IDF](https://github.com/espressif/esp-idf) configurado no Visual Studio Code
- Microcontrolador ESP32
- Sensor ultrassônico HC-SR04
- Conexão:
  - `TRIG_PIN` -> GPIO4 (Pino D2)
  - `ECHO_PIN` -> GPIO2 (Pino D4)

### Nota sobre a Alimentação do Sensor

O sensor HC-SR04 precisa de uma alimentação de 5V para funcionar corretamente. Como o ESP32 fornece apenas 3.3V nos pinos de saída, é necessário utilizar uma fonte externa de 5V para alimentar o sensor. Certifique-se de conectar o GND da fonte de 5V ao GND do ESP32 para garantir uma referência comum entre o sensor e o microcontrolador.

## Estrutura do Código

O código se divide nas seguintes funções:

1. **`init_ultrasonic_sensor`**: Configura os pinos TRIG e ECHO para o sensor.
2. **`measure_distance`**: Envia um pulso no TRIG e mede a resposta no ECHO, retornando a distância em centímetros. Inclui timeout para evitar bloqueios.
3. **`ultrasonic_task`**: Executa as leituras de distância em um loop com delay e mantém o *watchdog* atualizado para evitar timeouts.
4. **`app_main`**: Inicializa a tarefa `ultrasonic_task`.

## Código

```c
#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_timer.h"
#include "esp_task_wdt.h" // Para registro no watchdog

#define TRIG_PIN GPIO_NUM_4 // Pino D2
#define ECHO_PIN GPIO_NUM_2 // Pino D4
#define TIMEOUT_US 25000 // Reduzido para 25 ms para evitar delays longos

void init_ultrasonic_sensor() {
    gpio_set_direction(TRIG_PIN, GPIO_MODE_OUTPUT);
    gpio_set_direction(ECHO_PIN, GPIO_MODE_INPUT);
}

float measure_distance() {
    gpio_set_level(TRIG_PIN, 0);
    vTaskDelay(2 / portTICK_PERIOD_MS);
    gpio_set_level(TRIG_PIN, 1);
    esp_rom_delay_us(10);
    gpio_set_level(TRIG_PIN, 0);

    int64_t start_time = 0, end_time = 0;

    // Aguardar pelo sinal de subida, com timeout
    int64_t wait_start = esp_timer_get_time();
    while (gpio_get_level(ECHO_PIN) == 0) {
        if (esp_timer_get_time() - wait_start > TIMEOUT_US) {
            return -1.0; // Timeout
        }
        start_time = esp_timer_get_time();
    }

    // Aguardar pelo sinal de descida, com timeout
    wait_start = esp_timer_get_time();
    while (gpio_get_level(ECHO_PIN) == 1) {
        if (esp_timer_get_time() - wait_start > TIMEOUT_US) {
            return -1.0; // Timeout
        }
        end_time = esp_timer_get_time();
    }

    float duration = (float)(end_time - start_time);
    float distance = (duration * 0.034) / 2;
    return distance;
}

void ultrasonic_task(void *pvParameters) {
    init_ultrasonic_sensor();

    // Registra a tarefa no watchdog
    esp_task_wdt_add(NULL);

    while (1) {
        // Realiza a leitura de distância
        float distance = measure_distance();
        
        if (distance >= 0) {
            printf("Distância: %.2f cm\n", distance);
        }

        // Reseta o watchdog manualmente para evitar timeout
        esp_task_wdt_reset();

        // Delay de 1 segundo entre as leituras
        vTaskDelay(pdMS_TO_TICKS(1000));
    }

    // Remove a tarefa do watchdog ao finalizar (não deve ser necessário neste caso)
    esp_task_wdt_delete(NULL);
}

void app_main(void) {
    // Inicia a tarefa para o sensor ultrassônico
    xTaskCreate(ultrasonic_task, "ultrasonic_task", 2048, NULL, 5, NULL);
}
```
## Setup

![121312321](https://github.com/user-attachments/assets/cb05f079-cc3d-4578-a342-8cd138a5efc2)


## Teste do sensor

![image](https://github.com/user-attachments/assets/4bb9173d-967a-4fff-adf3-38bdb4777c03)

