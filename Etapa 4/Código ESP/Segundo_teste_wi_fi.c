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
#define YFS201_PIN GPIO_NUM_4
#define PULSOS_POR_LITRO 450
#define ULTRASONIC_TRIG_PIN GPIO_NUM_18
#define ULTRASONIC_ECHO_PIN GPIO_NUM_19
#define TIMEOUT_US 25000

// Credenciais Wi-Fi
#define WIFI_SSID "Laura M 2.4Ghz"
#define WIFI_PASS "*********"

// URL do servidor Python
#define SERVER_URL "http://192.168.0.15:5000/receive_data"

// Variáveis globais
volatile uint32_t contador_pulsos = 0;
static const char *TAG = "Main";

// Função de interrupção para o sensor YF-S201
static void IRAM_ATTR contar_pulsos(void *arg) {
    contador_pulsos++;
}

// Configuração do GPIO para o sensor YF-S201
void setup_yfs201_gpio() {
    gpio_config_t io_conf = {
        .intr_type = GPIO_INTR_POSEDGE,
        .mode = GPIO_MODE_INPUT,
        .pin_bit_mask = (1ULL << YFS201_PIN)
    };
    gpio_config(&io_conf);
    gpio_install_isr_service(0);
    gpio_isr_handler_add(YFS201_PIN, contar_pulsos, NULL);
}

// Inicializa o Wi-Fi
void wifi_init(void) {
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    ESP_LOGI(TAG, "Inicializando Wi-Fi...");
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    esp_netif_create_default_wifi_sta();

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));

    wifi_config_t wifi_config = {
        .sta = {
            .ssid = WIFI_SSID,
            .password = WIFI_PASS,
        },
    };
    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
    ESP_ERROR_CHECK(esp_wifi_set_config(ESP_IF_WIFI_STA, &wifi_config));
    ESP_ERROR_CHECK(esp_wifi_start());

    ESP_LOGI(TAG, "Conectando ao Wi-Fi...");
    ESP_ERROR_CHECK(esp_wifi_connect());
}

// Envia dados via HTTP POST
void send_data(float vazao, float volume_total, float distancia) {
    char payload[256];
    snprintf(payload, sizeof(payload), "{\"flow_rate\":%.2f,\"total_volume\":%.2f,\"distance\":%.2f}", vazao, volume_total, distancia);

    esp_http_client_config_t config = {
        .url = SERVER_URL,
        .method = HTTP_METHOD_POST,
    };

    esp_http_client_handle_t client = esp_http_client_init(&config);
    esp_http_client_set_header(client, "Content-Type", "application/json");
    esp_http_client_set_post_field(client, payload, strlen(payload));

    esp_err_t err = esp_http_client_perform(client);
    if (err == ESP_OK) {
        ESP_LOGI(TAG, "Dados enviados com sucesso: %s", payload);
    } else {
        ESP_LOGE(TAG, "Erro ao enviar dados: %s", esp_err_to_name(err));
    }

    esp_http_client_cleanup(client);
}

// Função de inicialização para o sensor ultrassônico
void init_ultrasonic_sensor() {
    gpio_set_direction(ULTRASONIC_TRIG_PIN, GPIO_MODE_OUTPUT);
    gpio_set_direction(ULTRASONIC_ECHO_PIN, GPIO_MODE_INPUT);
}

// Função para medir a distância usando o sensor ultrassônico
float measure_distance() {
    gpio_set_level(ULTRASONIC_TRIG_PIN, 0);
    vTaskDelay(2 / portTICK_PERIOD_MS);
    gpio_set_level(ULTRASONIC_TRIG_PIN, 1);
    esp_rom_delay_us(10);
    gpio_set_level(ULTRASONIC_TRIG_PIN, 0);

    int64_t start_time = 0, end_time = 0;
    int64_t wait_start = esp_timer_get_time();
    while (gpio_get_level(ULTRASONIC_ECHO_PIN) == 0) {
        if (esp_timer_get_time() - wait_start > TIMEOUT_US) {
            return -1.0;
        }
        start_time = esp_timer_get_time();
    }

    wait_start = esp_timer_get_time();
    while (gpio_get_level(ULTRASONIC_ECHO_PIN) == 1) {
        if (esp_timer_get_time() - wait_start > TIMEOUT_US) {
            return -1.0;
        }
        end_time = esp_timer_get_time();
    }

    float duration = (float)(end_time - start_time);
    float distance = (duration * 0.034) / 2;
    return distance;
}

// Tarefa de monitoramento dos sensores
void sensor_task(void *pvParameters) {
    setup_yfs201_gpio();
    init_ultrasonic_sensor();

    const float intervalo_segundos = 1.0;
    float volume_total = 0;

    while (1) {
        uint32_t pulsos = contador_pulsos;
        contador_pulsos = 0;
        vTaskDelay(pdMS_TO_TICKS(intervalo_segundos * 1000));

        float vazao = (pulsos / intervalo_segundos) * (60.0 / PULSOS_POR_LITRO);
        float volume = vazao / 60;
        volume_total += volume;

        float distancia = measure_distance();

        ESP_LOGI(TAG, "Vazão: %.2f L/min, Volume Total: %.2f L, Distância: %.2f cm", vazao, volume_total, distancia);

        // Envia os dados ao servidor
        send_data(vazao, volume_total, distancia);
    }
}

// Função principal
void app_main(void) {
    wifi_init();
    xTaskCreate(sensor_task, "sensor_task", 4096, NULL, 5, NULL);
}
