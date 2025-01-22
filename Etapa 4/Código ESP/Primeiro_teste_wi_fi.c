#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
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

// Credenciais Wi-Fi
#define WIFI_SSID "Laura M 2.4Ghz"
#define WIFI_PASS "13l31s16a"

// URL do servidor Python
#define SERVER_URL "http://192.168.0.18:5000/receive_data"

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
void send_data(float vazao, float volume_total) {
    char payload[128];
    snprintf(payload, sizeof(payload), "{\"flow_rate\":%.2f,\"total_volume\":%.2f}", vazao, volume_total);

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

// Tarefa de monitoramento do sensor
void flow_task(void *pvParameters) {
    setup_yfs201_gpio();
    const float intervalo_segundos = 1.0;
    float volume_total = 0;

    while (1) {
        uint32_t pulsos = contador_pulsos;
        contador_pulsos = 0;
        vTaskDelay(pdMS_TO_TICKS(intervalo_segundos * 1000));

        float vazao = (pulsos / intervalo_segundos) * (60.0 / PULSOS_POR_LITRO);
        float volume = vazao / 60;
        volume_total += volume;

        ESP_LOGI(TAG, "Vazão: %.2f L/min, Volume Total: %.2f L", vazao, volume_total);

        // Envia os dados ao servidor
        send_data(vazao, volume_total);
    }
}

// Função principal
void app_main(void) {
    // Inicializa o Wi-Fi
    wifi_init();

    // Cria a tarefa do sensor de vazão
    xTaskCreate(flow_task, "flow_task", 4096, NULL, 5, NULL);
}
