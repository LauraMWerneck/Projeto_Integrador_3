//-----------------------------------------------------------------------------------------------------------
// Name        : sensor_vazao.c
// Author      : Laura Martin Werneck
// Date        : 07/11/2024
// Description : Código para controle do sensor de vazão YF-S201. Este código recebe os pulsos gerados 
// pelo sensor durante a passagem de água e calcula a vazão com base nesses pulsos e no fator de calibração 
// correspondente. O código apresenta os resultados do teste, exibindo a vazão em litros por minuto e litros 
// por hora, além de informar o volume total de água que passou pelo sensor desde o início do sistema.
//------------------------------------------------------------------------------------------------------------

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
    float vazao_litros_por_hora = 0;
    float volume = 0;
    float volume_total = 0;
   
    // Intervalo de tempo em segundos para calcular a vazão
    const float intervalo_segundos = 1.0;
   
    while (1) {
        // Salva o contador de pulsos e zera para próxima medição
        pulso_inicial = contador_pulsos;
        contador_pulsos = 0;
       
        // Aguarda o intervalo de tempo especificado
        vTaskDelay((int)(intervalo_segundos * 1000) / portTICK_PERIOD_MS);
       
        // Calculo da vazão em litros por minuto
        vazao_litros_por_minuto = (pulso_inicial / intervalo_segundos) * (60.0 / PULSOS_POR_LITRO);

        // Calculo da vazão em litros por hora
        vazao_litros_por_hora = vazao_litros_por_minuto * 60.0;
       
        // Acumulo do volume total de água
        volume = vazao_litros_por_minuto/60;
        volume_total = volume_total + volume;

        // Exibe o resultado
        printf("Vazão (L/min): %.2f L/min\n", vazao_litros_por_minuto);
        printf("Vazão (L/h): %.2f L/h\n", vazao_litros_por_hora);
        printf("Volume Total: %.2f litros\n", volume_total);
    }
}

void app_main() {
    setup_gpio();           // Configura o pino GPIO e a interrupção
    medir_vazao();          // Inicia a medição da vazão de água
}
