#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_timer.h"
#include "esp_log.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "nvs_flash.h"
#include "esp_http_client.h"

// Configurações do sensor
#define YFS201_PIN GPIO_NUM_4          // Pino conectado ao sensor de fluxo YF-S201
#define PULSOS_POR_LITRO 450           // Número de pulsos que correspondem a 1 litro de fluxo
#define ULTRASONIC_TRIG_PIN GPIO_NUM_18 // Pino TRIG do sensor ultrassônico
#define ULTRASONIC_ECHO_PIN GPIO_NUM_19 // Pino ECHO do sensor ultrassônico
#define TIMEOUT_US 25000               // Tempo máximo de espera para leitura do sensor ultrassônico

// Credenciais Wi-Fi
#define WIFI_SSID "TP-Link_A25C"     // Nome da rede Wi-Fi
#define WIFI_PASS "62530095"          // Senha da rede Wi-Fi

// URL do servidor Python
#define SERVER_URL "http://192.168.0.103:5000/ESP_data" // Endereço do backend

// Variáveis globais
volatile uint32_t contador_pulsos = 0; // Variável que armazena a contagem de pulsos do sensor de fluxo
static const char *TAG = "Main";       // Tag para exibição de logs

// Função de interrupção para o sensor YF-S201
static void IRAM_ATTR contar_pulsos(void *arg) {
    contador_pulsos++; // Incrementa o contador de pulsos toda vez que o sensor gera um pulso
}

// Configuração do GPIO para o sensor YF-S201
void setup_yfs201_gpio() {
    gpio_config_t io_conf = {              // Configura o pino do sensor como entrada com interrupção
        .intr_type = GPIO_INTR_POSEDGE,    // Interrupção no flanco de subida
        .mode = GPIO_MODE_INPUT,           // Configuração como entrada
        .pin_bit_mask = (1ULL << YFS201_PIN) // Máscara do pino
    };
    gpio_config(&io_conf);                 // Aplica as configurações
    gpio_install_isr_service(0);           // Inicializa o serviço de interrupções
    gpio_isr_handler_add(YFS201_PIN, contar_pulsos, NULL); // Associa a interrupção ao pino
}

// Inicializa o Wi-Fi
void wifi_init(void) {
    esp_err_t ret = nvs_flash_init(); // Inicializa o sistema de armazenamento não volátil
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase()); // Apaga o armazenamento se necessário
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    ESP_LOGI(TAG, "Inicializando Wi-Fi...");
    ESP_ERROR_CHECK(esp_netif_init()); // Inicializa a interface de rede
    ESP_ERROR_CHECK(esp_event_loop_create_default()); // Cria o loop de eventos padrão
    esp_netif_create_default_wifi_sta(); // Cria uma interface Wi-Fi no modo estação

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT(); // Configurações padrão de inicialização
    ESP_ERROR_CHECK(esp_wifi_init(&cfg)); // Inicializa o módulo Wi-Fi

    wifi_config_t wifi_config = {         // Configura as credenciais Wi-Fi
        .sta = {
            .ssid = WIFI_SSID,
            .password = WIFI_PASS,
        },
    };
    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA)); // Define o modo como estação
    ESP_ERROR_CHECK(esp_wifi_set_config(ESP_IF_WIFI_STA, &wifi_config)); // Aplica as credenciais
    ESP_ERROR_CHECK(esp_wifi_start()); // Inicia o Wi-Fi

    ESP_LOGI(TAG, "Conectando ao Wi-Fi...");
    ESP_ERROR_CHECK(esp_wifi_connect()); // Conecta à rede Wi-Fi
}

// Envia dados via HTTP POST
void send_data(float vazao, float volume_total, float distancia, float volume_por_minuto) {
    char payload[256]; // Buffer para armazenar os dados em formato JSON
    snprintf(payload, sizeof(payload), "{\"flow_rate\":%.2f,\"total_volume\":%.2f,\"distance\":%.2f,\"volume_minuto\":%.2f}", vazao, volume_total, distancia, volume_por_minuto);

    esp_http_client_config_t config = { // Configura o cliente HTTP
        .url = SERVER_URL,
        .method = HTTP_METHOD_POST,
    };

    esp_http_client_handle_t client = esp_http_client_init(&config); // Inicializa o cliente HTTP
    esp_http_client_set_header(client, "Content-Type", "application/json"); // Define o cabeçalho como JSON
    esp_http_client_set_post_field(client, payload, strlen(payload)); // Define o corpo da requisição

    esp_err_t err = esp_http_client_perform(client); // Realiza a requisição
    if (err == ESP_OK) {
        ESP_LOGI(TAG, "Dados enviados com sucesso: %s", payload); // Log de sucesso
    } else {
        ESP_LOGE(TAG, "Erro ao enviar dados: %s", esp_err_to_name(err)); // Log de erro
    }

    esp_http_client_cleanup(client); // Libera os recursos do cliente HTTP
}

// Função de inicialização para o sensor ultrassônico
void init_ultrasonic_sensor() {
    gpio_set_direction(ULTRASONIC_TRIG_PIN, GPIO_MODE_OUTPUT); // Configura o pino TRIG como saída
    gpio_set_direction(ULTRASONIC_ECHO_PIN, GPIO_MODE_INPUT);  // Configura o pino ECHO como entrada
}

// Função para medir a distância usando o sensor ultrassônico
float measure_distance() {
    gpio_set_level(ULTRASONIC_TRIG_PIN, 0); // Garante que o TRIG está em nível baixo
    vTaskDelay(2 / portTICK_PERIOD_MS);     // Aguarda 2ms
    gpio_set_level(ULTRASONIC_TRIG_PIN, 1); // Envia um pulso de 10µs no TRIG
    esp_rom_delay_us(10);
    gpio_set_level(ULTRASONIC_TRIG_PIN, 0);

    int64_t start_time = 0, end_time = 0; // Variáveis para medir o tempo do pulso
    int64_t wait_start = esp_timer_get_time();
    while (gpio_get_level(ULTRASONIC_ECHO_PIN) == 0) { // Espera o ECHO subir
        if (esp_timer_get_time() - wait_start > TIMEOUT_US) { // Verifica timeout
            return -1.0; // Retorna erro se ultrapassar o tempo limite
        }
        start_time = esp_timer_get_time();
    }

    wait_start = esp_timer_get_time();
    while (gpio_get_level(ULTRASONIC_ECHO_PIN) == 1) { // Espera o ECHO descer
        if (esp_timer_get_time() - wait_start > TIMEOUT_US) { // Verifica timeout
            return -1.0; // Retorna erro se ultrapassar o tempo limite
        }
        end_time = esp_timer_get_time();
    }

    float duration = (float)(end_time - start_time); // Calcula a duração do pulso
    float distance = (duration * 0.034) / 2; // Calcula a distância em cm
    return distance;
}

// Tarefa de monitoramento dos sensores
void sensor_task(void *pvParameters) {
    setup_yfs201_gpio();         // Configura o sensor de fluxo
    init_ultrasonic_sensor();    // Configura o sensor ultrassônico

    const float intervalo_segundos = 1.0; // Intervalo de leitura dos sensores (1 segundo)
    float volume_total = 0;               // Volume total acumulado

    while (1) {
        uint32_t pulsos = contador_pulsos; // Copia os pulsos capturados
        contador_pulsos = 0;               // Reseta o contador
        vTaskDelay(pdMS_TO_TICKS(intervalo_segundos * 1000)); // Aguarda o intervalo

        float vazao = (pulsos / intervalo_segundos) * (60.0 / PULSOS_POR_LITRO); // Calcula a vazão em L/min
        float volume = vazao / 60;        // Calcula o volume em litros
        float volume_por_minuto = 0;                  // Volume salvo a cada minuto
        volume_total += volume;          // Atualiza o volume total acumulado
        float distancia = measure_distance(); // Mede a distância com o sensor ultrassônico

           // A cada minuto, salva o volume em uma variável
        static int segundos = 0;
        segundos++;
        
        ESP_LOGI(TAG, "Vazão: %.2f L/min, Volume Total: %.2f L, Distância: %.2f cm", vazao, volume_total, distancia);

        if (segundos >= 60) { // Após 60 segundos
            volume_por_minuto = volume_total;       // Salva o volume total no minuto
            printf("Volume salvo a cada minuto: %.2f litros\n", volume_por_minuto);
            ESP_LOGI(TAG, "Volume por minuto: %.2f L", volume_por_minuto);

            send_data(vazao, volume_total, distancia, volume_por_minuto);
            volume_por_minuto = 0;                 // Reseta o volume_por_minuto após exibir
            volume_total = 0;                      // Opcional: Reseta volume_total, se necessário
            segundos = 0;                          // Reseta o contador de segundos
        }
    }
}

// Função principal
void app_main(void) {
    wifi_init(); // Inicializa o Wi-Fi
    xTaskCreate(sensor_task, "sensor_task", 4096, NULL, 5, NULL); // Cria a tarefa de monitoramento dos sensores
}
