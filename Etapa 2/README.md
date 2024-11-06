# Resumo do que foi desenvolvido na Etapa 2

## Determinação das Fórmulas do Aplicativo

### Dados Retornados pelo Microcontrolador
O microcontrolador envia dados para o backend, usados para calcular o custo da água na região, com base nas informações da conta de água inseridas pelo usuário.

### Cálculos no Aplicativo

1. **Consumo em Reais**: Calculado considerando a hora e data.
2. **Água Disponível na Caixa d’Água**: Cálculo baseado na quantidade de água.
3. **Consumo Real**: Diferença entre o valor calculado e o hidrômetro.
4. **Tempo de Água Disponível**: Calculado com base no consumo dos últimos 3 dias.
5. **Expectativa de Consumo**: Estimativa para o próximo mês, após o primeiro mês de uso.
6. **Gasto no Próximo Mês**: Usuário define o limite, disponível após o primeiro mês.

### Funcionalidades Sem Fórmulas
- **Limitar Aviso**: Notifica sobre excesso de gasto.
- **Próxima Manutenção**: Notifica a data da próxima manutenção.

## Especificações do Sensor de Vazão YF-S201

### Descrição
O YF-S201 é um sensor de vazão de água utilizado em projetos eletrônicos e industriais para medir o fluxo de líquidos. Ele é simples, de baixo custo e funciona detectando pulsos gerados por um rotor acionado pelo fluxo de água.

### Especificações Técnicas
- **Faixa de Medição**: 1 a 30 L/min
- **Tensão de Operação**: 5 a 18V
- **Corrente Máxima**: 15 mA
- **Temperatura**: -25°C a 80°C
- **Pressão Máxima**: 1,75 MPa
- **Conexão**: Rosca G1/2" (uso doméstico e industrial)

### Funcionamento
A água aciona um rotor que gera pulsos detectados por um sensor de efeito Hall. Cada 450 pulsos representam 1 litro de água. A vazão pode ser calculada com a fórmula:

Fluxo (L/min) = Frequência de Pulsos (Hz) / 7,5

## Desenvolvimento de Firmware para Comunicação com o Sensor YF-S201

### Objetivo
O objetivo foi testar a comunicação entre o sensor YF-S201 e o microcontrolador ESP32 para medir a vazão de água. O firmware foi desenvolvido para ler e processar os pulsos gerados pelo sensor e calcular a vazão em litros por minuto.

### Funcionamento
- O sensor gera pulsos que são capturados pelo pino GPIO da ESP32.
- Cada pulso corresponde a uma quantidade específica de água, definida pela constante **PULSOS_POR_LITRO (450 pulsos por litro)**.
- A vazão é calculada a partir da frequência dos pulsos.

### Código de Teste
O código configura o pino GPIO4 da ESP32, instala uma interrupção para contar os pulsos, e calcula a vazão com base nos pulsos detectados.

### Resultados
O sistema exibe a vazão em tempo real no monitor serial da ESP32. Inicialmente, o teste foi feito utilizando vento para girar o rotor do sensor.

## Especificações do Sensor Ultrassônico HC-SR04

### Descrição
O HC-SR04 é um sensor ultrassônico usado para medir distâncias e é amplamente aplicado em projetos de controle de nível de líquidos. Ele emite ondas ultrassônicas que retornam após atingirem a superfície do líquido, permitindo calcular a distância.

### Especificações Técnicas
- **Distância de Medição**: 2 cm a 4 m
- **Tensão de Operação**: 5V
- **Precisão**: Aproximadamente 3 mm
- **Frequência**: 40 kHz
- **Função**: Ideal para monitoramento e controle de nível de água em reservatórios e caixas d'água.

# Desenvolvimento de Firmware para Comunicação com o Sensor Ultrassônico HC-SR04

Nesta etapa, foi implementada a medição de distância utilizando o sensor ultrassônico HC-SR04 com o microcontrolador ESP32, através do framework ESP-IDF no Visual Studio Code. O objetivo era medir a distância até a superfície da água, utilizando o sensor para controle de nível de líquidos.

### Configuração e Conexões
- O sensor HC-SR04 foi conectado ao ESP32, com o pino **TRIG** no GPIO4 e o pino **ECHO** no GPIO2.
- Como o sensor exige 5V para alimentação, foi utilizada uma fonte externa de 5V, com o GND conectado ao GND do ESP32.

### Estrutura do Código
- A função **`init_ultrasonic_sensor`** configura os pinos TRIG e ECHO.
- **`measure_distance`** envia um pulso no pino TRIG e calcula o tempo de resposta no pino ECHO, utilizando esse tempo para calcular a distância.
- **`ultrasonic_task`** é responsável por realizar a leitura contínua da distância em intervalos de 1 segundo, com um sistema de watchdog para evitar travamentos.
- A função **`app_main`** inicializa a tarefa de leitura do sensor.

Com a implementação concluída, o sistema realiza a medição da distância e exibe o resultado em tempo real no monitor serial.

## Descrição do Sistema Físico de Teste

O sistema de teste será composto por três componentes principais: sensor de vazão YF-S201, válvula solenoide e sensor ultrassônico. A ESP32 será responsável por controlar os sensores e acionar a válvula.

### Estrutura do Sistema:
- **Mangueira transparente** conectada ao registro de água.
- **Sensor de vazão** YF-S201 e **válvula solenoide** acoplados a uma peça 3D para controle do fluxo de água.
- **Balde** representando a caixa d'água, com válvula de saída para simulação de vazão.
- **Sensor ultrassônico** montado na tampa do balde para medir o nível de água.

O sistema conta com um segundo balde para escoar a água durante os testes. Para otimizar a conexão entre a válvula e o sensor de vazão, foi projetada uma peça personalizada em 3D para corrigir a discrepância nos diâmetros internos, prevenindo problemas como cavitação.





