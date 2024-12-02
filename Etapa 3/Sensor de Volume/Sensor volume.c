#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"
#include "driver/gpio.h"
#include "esp_timer.h"
#include "esp_task_wdt.h"
#include "driver/uart.h"

// Configurações do sensor ultrassônico
#define TRIG_PIN GPIO_NUM_19
#define ECHO_PIN GPIO_NUM_18
#define TIMEOUT_US 25000

// Configurações do sensor de vazão
#define YFS201_PIN GPIO_NUM_4
#define PULSOS_POR_LITRO 450

// Configurações da UART
#define UART_NUM UART_NUM_0
#define BUF_SIZE 1024

float offset = 0.0;             // Variável global para ajuste de distância
SemaphoreHandle_t mutex_offset; // Mutex para proteger o acesso ao offset
bool adjust_offset = false;     // Flag para ajuste do ponto zero

volatile uint32_t contador_pulsos = 0; // Contador de pulsos do sensor de vazão

// Função da interrupção para o sensor de vazão
static void IRAM_ATTR contar_pulsos(void *arg) {
    contador_pulsos++;
}

// Configuração do sensor ultrassônico
void init_ultrasonic_sensor() {
    gpio_set_direction(TRIG_PIN, GPIO_MODE_OUTPUT);
    gpio_set_direction(ECHO_PIN, GPIO_MODE_INPUT);
}

// Função para medir distância
float measure_distance() {
    gpio_set_level(TRIG_PIN, 0);
    vTaskDelay(2 / portTICK_PERIOD_MS);
    gpio_set_level(TRIG_PIN, 1);
    esp_rom_delay_us(10);
    gpio_set_level(TRIG_PIN, 0);

    int64_t start_time = 0, end_time = 0;

    int64_t wait_start = esp_timer_get_time();
    while (gpio_get_level(ECHO_PIN) == 0) {
        if (esp_timer_get_time() - wait_start > TIMEOUT_US) {
            return -1.0;
        }
        start_time = esp_timer_get_time();
    }

    wait_start = esp_timer_get_time();
    while (gpio_get_level(ECHO_PIN) == 1) {
        if (esp_timer_get_time() - wait_start > TIMEOUT_US) {
            return -1.0;
        }
        end_time = esp_timer_get_time();
    }

    float duration = (float)(end_time - start_time);
    float distance = (duration * 0.034) / 2;
    return distance;
}

// Tarefa para o sensor ultrassônico
void ultrasonic_task(void *pvParameters) {
    init_ultrasonic_sensor();
    esp_task_wdt_add(NULL);

    while (1) {
        float distance = measure_distance();

        if (distance >= 0) {
            float adjusted_distance;

            xSemaphoreTake(mutex_offset, portMAX_DELAY);
            if (adjust_offset) {
                offset = distance;
                adjust_offset = false;
                printf("Ponto de referência ajustado para: %.2f cm\n", offset);
            }
            adjusted_distance = offset - distance;
            xSemaphoreGive(mutex_offset);

            printf("Distância ajustada: %.2f cm\n", adjusted_distance);
        } else {
            printf("Erro ao medir distância.\n");
        }

        esp_task_wdt_reset();
        vTaskDelay(pdMS_TO_TICKS(1000));
    }

    esp_task_wdt_delete(NULL);
}

// Configuração do GPIO para o sensor de vazão
void setup_flow_sensor() {
    gpio_config_t io_conf = {
        .intr_type = GPIO_INTR_POSEDGE,
        .mode = GPIO_MODE_INPUT,
        .pin_bit_mask = (1ULL << YFS201_PIN)
    };
    gpio_config(&io_conf);
    gpio_install_isr_service(0);
    gpio_isr_handler_add(YFS201_PIN, contar_pulsos, NULL);
}

// Tarefa para medir a vazão de água
void flow_sensor_task(void *pvParameters) {
    setup_flow_sensor();

    const float intervalo_segundos = 1.0;
    while (1) {
        uint32_t pulso_inicial = contador_pulsos;
        contador_pulsos = 0;

        vTaskDelay((int)(intervalo_segundos * 1000) / portTICK_PERIOD_MS);

        float vazao_litros_por_minuto = (pulso_inicial / intervalo_segundos) * (60.0 / PULSOS_POR_LITRO);
        printf("Vazão: %.2f L/min\n", vazao_litros_por_minuto);
    }
}

// Tarefa para comunicação via UART
void uart_task(void *pvParameters) {
    uint8_t data[BUF_SIZE];

    uart_config_t uart_config = {
        .baud_rate = 115200,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE
    };
    uart_param_config(UART_NUM, &uart_config);
    uart_driver_install(UART_NUM, BUF_SIZE * 2, 0, 0, NULL, 0);

    while (1) {
        int len = uart_read_bytes(UART_NUM, data, BUF_SIZE, 20 / portTICK_PERIOD_MS);
        if (len > 0) {
            data[len] = '\0';
            if (data[0] == '1') {
                xSemaphoreTake(mutex_offset, portMAX_DELAY);
                adjust_offset = true;
                xSemaphoreGive(mutex_offset);
            }
        }
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}

// Função principal
void app_main(void) {
    mutex_offset = xSemaphoreCreateMutex();

    xTaskCreate(ultrasonic_task, "ultrasonic_task", 4096, NULL, 5, NULL);
    xTaskCreate(flow_sensor_task, "flow_sensor_task", 2048, NULL, 5, NULL);
    xTaskCreate(uart_task, "uart_task", 2048, NULL, 5, NULL);
}
