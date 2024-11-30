# Teste Individual do Sensor de Vazão

Nesta etapa, foi realizado um teste individual do ensor de vazão (YF-S201) para validar seu funcionamento e verificar se o fator de calibração estava correto, garantindo que ele apresentasse um valor real do volume de água que passou pelo sensor. Para isso, foi desenvolvido um código capaz de receber os pulsos gerados pelo sensor durante a passagem de água e calcular a vazão com base nesses pulsos e no fator de calibração correspondente. O código apresenta os resultados do teste, exibindo a vazão em litros por minuto e litros por hora, além de informar o volume total de água que passou pelo sensor desde o início do sistema. 

## Documentação do Código

### Dependências/Bibliotecas Incluídas:
- `<stdio.h>`: Para funções de entrada e saída (ex.: `printf`).
- `<stdint.h>`: Para tipos de dados de largura fixa (ex.: `uint32_t`).
- `<stdbool.h>`: Para uso do tipo `bool`.
- `freertos/FreeRTOS.h` e `freertos/task.h`: Para usar o sistema operacional FreeRTOS, que permite multitarefa.
- `driver/gpio.h`: Para manipular pinos GPIO do ESP32.
- `esp_timer.h`: Para operações relacionadas a temporização.

### Constantes
- `YFS201_PIN`: Define o pino GPIO usado para conectar o sensor (GPIO_NUM_4).
- `PULSOS_POR_LITRO`: Especifica o número de pulsos gerados pelo sensor YF-S201 por litro de água (450 pulsos/litro).

### Variáveis Globais
- `contador_pulsos`: Variável volátil que armazena o número de pulsos detectados pelo sensor. É declarada como `volatile` porque seu valor pode ser alterado pela interrupção.

### Funções

- `contar_pulsos(void* arg)`: Função de interrupção que incrementa o contador de pulsos toda vez que o sensor gera um sinal. É declarada como `IRAM_ATTR` para garantir execução rápida diretamente na RAM. Seu comportamento baseia-se em incrementa a variável `contador_pulsos`.

- `setup_gpio()`: Configura o GPIO usado pelo sensor e registra a função de interrupção.
 
- `medir_vazao()`: Calcula a vazão e o volume total de água, exibindo os resultados em intervalos regulares. Essa função salva e reseta o valor do contador de pulsos a cada intervalo, além de aguardar o tempo definido em `intervalo_segundos` antes de calcular a vazão. O cálculo da vzão é medido pela seguinte fórmula:

Vazão (L/min) = (pulsos/tempo)*(60/PULSOS_POR\LITRO)
    
A Vazão (L/h) é calculada pela multiplicação da vazão em L/min por 60, e o volume total pela soma do volume incremental ao longo do tempo. Ao final dos cálculos a função exibe os resultados no terminal usando `printf`.

- `app_main()`: Função principal executada ao iniciar o microcontrolador. Ela configura o GPIO do sensor com `setup_gpio()` e inicia o cálculo contínuo de vazão com `medir_vazao()`.

### Fluxo do Programa
1. Configura o GPIO e registra a interrupção para o sensor.
2. Em `medir_vazao()`, realiza os seguintes passos continuamente:
   - Coleta e reseta o número de pulsos detectados.
   - Aguarda um intervalo de tempo fixo (1 segundo).
   - Calcula a vazão em L/min e L/h, bem como o volume acumulado.
   - Imprime os resultados.
   
### Saída
Durante a execução, o programa exibe no terminal:
- Vazão em Litros por Minuto (L/min).
- Vazão em Litros por Hora (L/h).
- Volume total acumulado em Litros.
Abaixo está uma imagem ilustrando como os dados são exibidos no monitor serial:

FOTO

## Resultados Obtidos com o Teste

Inicialmente, o teste foi realizado alimentando o sensor com 3.3V, porém, notamos que nessa condição ele não apresentava uma calibração precisa. Por isso, decidimos realizar o teste utilizando 5V, conforme indicado e recomendado no datasheet do sensor. Ao usar 5V como fonte de alimentação, o sensor funcionou perfeitamente. Para fornecer os 5V necessários, utilizamos um módulo conversor de tensão DC/DC Step-Up.

Para realizar o teste, utilizou-se o sistema físico de teste construído, composto por dois baldes, uma bomba de água e tubulações. O sistema funciona da seguinte maneira: o balde inferior, cheio de água, alimenta a bomba que, por meio de uma mangueira conectada ao sensor, bombeia a água. Após passar pelo sensor, a água é conduzida por outra mangueira que a despeja no balde superior.

Os baldes utilizados possuem marcações para indicar seus volumes. O teste foi iniciado com o balde superior contendo 1 litro de água. Quando o sensor foi ativado pela passagem de água bombeada, enchemos o balde até atingir a marcação de 4 litros. Como o balde já possuía 1 litro inicialmente, a quantidade de água que passou pelo sensor foi de 3 litros. O valor exibido no monitor serial confirmou essa quantidade, validando o funcionamento do sensor e demonstrando que ele está devidamente calibrado. Um vídeo gravado mostrando esse teste é apresentado abaixo:



https://github.com/user-attachments/assets/b91e898c-fdaf-4a9f-a3ad-da1b1ff82ab5


