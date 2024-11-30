#include <stdio.h>                    // Biblioteca padrão para entrada e saída
#include <stdint.h>                   // Tipos de dados inteiros padrão
#include <stdbool.h>                  // Tipos booleanos (true/false)
#include "freertos/FreeRTOS.h"        // Biblioteca do FreeRTOS para gerenciamento de tarefas
#include "freertos/task.h"            // Biblioteca do FreeRTOS para criação de tarefas
#include "driver/gpio.h"              // Biblioteca para manipulação de GPIOs
#include "esp_timer.h"                // Biblioteca para temporizadores de alta precisão
#include "esp_task_wdt.h"             // Biblioteca para o watchdog timer

// Definições de pinos para os sensores
#define ULTRASONIC_TRIG_PIN GPIO_NUM_18  // Pino GPIO para o TRIG do sensor ultrassônico
#define ULTRASONIC_ECHO_PIN GPIO_NUM_19  // Pino GPIO para o ECHO do sensor ultrassônico
#define YFS201_PIN GPIO_NUM_4            // Pino GPIO para o sensor de vazão YF-S201
#define TIMEOUT_US 25000                 // Timeout para medir distância (em microssegundos)

// Configuração do sensor de vazão YF-S201
#define PULSOS_POR_LITRO 450             // Quantidade de pulsos por litro do sensor YF-S201

// Variáveis globais
volatile uint32_t contador_pulsos = 0;    // Contador de pulsos do sensor YF-S201
TaskHandle_t ultrasonicTaskHandle = NULL; // Handle da tarefa do sensor ultrassônico
TaskHandle_t flowTaskHandle = NULL;       // Handle da tarefa do sensor de vazão

// Função de interrupção para o sensor YF-S201 (executada a cada pulso recebido)
static void IRAM_ATTR contar_pulsos(void* arg) {
    contador_pulsos++; // Incrementa o contador de pulsos global
}

// Função de inicialização para o sensor ultrassônico
void init_ultrasonic_sensor() {
    gpio_set_direction(ULTRASONIC_TRIG_PIN, GPIO_MODE_OUTPUT); // Define TRIG como saída
    gpio_set_direction(ULTRASONIC_ECHO_PIN, GPIO_MODE_INPUT);  // Define ECHO como entrada
}

// Função para medir a distância usando o sensor ultrassônico
float measure_distance() {
    // Gera o pulso de TRIG
    gpio_set_level(ULTRASONIC_TRIG_PIN, 0);           // TRIG em nível baixo
    vTaskDelay(2 / portTICK_PERIOD_MS);               // Aguarda 2 ms
    gpio_set_level(ULTRASONIC_TRIG_PIN, 1);           // TRIG em nível alto
    esp_rom_delay_us(10);                             // Mantém o pulso por 10 µs
    gpio_set_level(ULTRASONIC_TRIG_PIN, 0);           // TRIG em nível baixo

    int64_t start_time = 0, end_time = 0;             // Variáveis para armazenar os tempos de subida e descida

    // Aguarda pelo sinal de subida no ECHO (início da medição)
    int64_t wait_start = esp_timer_get_time();        // Tempo atual em microssegundos
    while (gpio_get_level(ULTRASONIC_ECHO_PIN) == 0) {
        if (esp_timer_get_time() - wait_start > TIMEOUT_US) {
            return -1.0; // Retorna -1 em caso de timeout
        }
        start_time = esp_timer_get_time();            // Registra o tempo de início
    }

    // Aguarda pelo sinal de descida no ECHO (fim da medição)
    wait_start = esp_timer_get_time();                // Reinicia o tempo de espera
    while (gpio_get_level(ULTRASONIC_ECHO_PIN) == 1) {
        if (esp_timer_get_time() - wait_start > TIMEOUT_US) {
            return -1.0; // Retorna -1 em caso de timeout
        }
        end_time = esp_timer_get_time();              // Registra o tempo de término
    }

    float duration = (float)(end_time - start_time);  // Calcula a duração do pulso em microssegundos
    float distance = (duration * 0.034) / 2;          // Calcula a distância em centímetros
    return distance;                                  // Retorna a distância medida
}

// Tarefa para o sensor ultrassônico
void ultrasonic_task(void *pvParameters) {
    init_ultrasonic_sensor();                        // Inicializa os pinos do sensor ultrassônico
    esp_task_wdt_add(NULL);                          // Registra a tarefa no watchdog

    while (1) {
        float distance = measure_distance();         // Mede a distância
        if (distance >= 0) {
            printf("Distância: %.2f cm\n", distance);// Imprime a distância medida
        }
        esp_task_wdt_reset();                        // Reseta o watchdog para evitar timeout
        vTaskDelay(pdMS_TO_TICKS(1000));             // Aguarda 1 segundo para a próxima leitura
    }
}

// Função para configurar o GPIO do sensor YF-S201
void setup_yfs201_gpio() {
    gpio_config_t io_conf = {
        .intr_type = GPIO_INTR_POSEDGE,                    // Interrupção na borda de subida
        .mode = GPIO_MODE_INPUT,                           // Define o pino como entrada
        .pin_bit_mask = (1ULL << YFS201_PIN)               // Máscara para selecionar o pino do sensor
    };
    gpio_config(&io_conf);                                 // Aplica as configurações
    gpio_install_isr_service(0);                           // Inicia o serviço de interrupção
    gpio_isr_handler_add(YFS201_PIN, contar_pulsos, NULL); // Adiciona a função de interrupção
}

// Tarefa para medir a vazão de água
void flow_task(void *pvParameters) {
    setup_yfs201_gpio();                           // Configura o GPIO do sensor
    float volume_total = 0;                        // Volume total acumulado
    const float intervalo_segundos = 1.0;          // Intervalo para cálculo (em segundos)

    while (1) {
        uint32_t pulso_inicial = contador_pulsos;  // Salva o contador de pulsos
        contador_pulsos = 0;                       // Reseta o contador para a próxima medição

        vTaskDelay((int)(intervalo_segundos * 1000) / portTICK_PERIOD_MS); // Aguarda o intervalo

        float vazao_litros_por_minuto = (pulso_inicial / intervalo_segundos) * (60.0 / PULSOS_POR_LITRO); // Calcula a vazão
        float volume = vazao_litros_por_minuto / 60; // Calcula o volume no intervalo
        volume_total += volume;                      // Acumula o volume total

        printf("Vazão (L/min): %.2f L/min\n", vazao_litros_por_minuto); // Exibe a vazão
        printf("Volume Total: %.2f litros\n", volume_total);            // Exibe o volume total
    }
}

// Tarefa de supervisão (prioridade máxima)
void supervisor_task(void *pvParameters) {
    printf("Tarefa de supervisão iniciada\n");

    // Cria as tarefas dos sensores
    xTaskCreate(ultrasonic_task, "ultrasonic_task", 2048, NULL, 5, &ultrasonicTaskHandle); // Tarefa do ultrassônico
    xTaskCreate(flow_task, "flow_task", 2048, NULL, 5, &flowTaskHandle);                   // Tarefa do sensor de vazão

    while (1) {
        printf("Supervisão ativa: monitorando sensores\n"); // Mensagem de status
        vTaskDelay(pdMS_TO_TICKS(2000));                    // Delay de 2 segundos
    }
}

// Função principal
void app_main(void) {
    // Cria a tarefa de supervisão com prioridade máxima
    xTaskCreate(supervisor_task, "supervisor_task", 2048, NULL, 10, NULL);
}
