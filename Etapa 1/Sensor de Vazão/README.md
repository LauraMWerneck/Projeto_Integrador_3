# Escolha do Sensor de Vazão de Água

Este documento apresenta um resumo do conhecimento adquirido nas pesquisas realizadas para a seleção do sensor de vazão de água mais adequado ao monitoramento e controle do sistema hidráulico proposto no projeto. O sensor selecionado foi o **YF-S201 G1/2**, escolhido por suas especificações técnicas e compatibilidade com o microcontrolador ESP32.

## Sensor de Vazão YF-S201 G1/2

### Especificações Técnicas
- **Faixa de medição**: 1 a 30 litros por minuto (l/min)
- **Conexão**: Rosca padrão G1/2", adequada para sistemas domésticos e industriais
- **Tensão de operação**: 5 a 18V DC
- **Sinal de saída**: Pulsos digitais lidos por microcontroladores
- **Funcionamento**: Utiliza uma turbina com ímã e sensor de efeito Hall para detectar a rotação e gerar um sinal proporcional à vazão
- **Compatibilidade**: Funciona bem com o ESP32, que utiliza 3.3V nos pinos digitais

### Funcionamento
O sensor YF-S201 mede a vazão da água utilizando uma turbina interna. À medida que a água passa, a turbina gira, e o sensor de efeito Hall detecta essas rotações, gerando pulsos que podem ser convertidos em uma leitura de vazão pelo microcontrolador.

Cada pulso gerado pelo sensor corresponde a uma quantidade específica de água. Por exemplo, no YF-S201, são cerca de 450 pulsos por litro de água. A fórmula para calcular a vazão em l/min é baseada na contagem dos pulsos em um determinado intervalo de tempo.

### Conexão com ESP32
- **VCC**: Conectar ao 5V do ESP32
- **GND**: Conectar ao GND do ESP32
- **Sinal**: Conectar a um pino digital do ESP32

O sensor, mesmo operando com 5V, é compatível com os pinos de 3.3V do ESP32.

### Modelos Comparados
| **Modelo**  | **YF-S201**          | **YF-S403**        | **YF-S401**        |
|-------------|----------------------|--------------------|--------------------|
| **Tensão de funcionamento** | DC 4.5V ~ 18V      | DC 4.5V ~ 18V      | 5 a 24V DC         |
| **Tensão de trabalho**       | DC 4.5V            | DC 4.5V            | 4.5V DC            |
| **Corrente máxima de trabalho** | 15mA (DC 5V)      | 15mA (DC 5V)       | 15mA (DC 5V)       |
| **Vazão de água**            | 1 ~ 30 L/min       | 1 ~ 60 L/min       | 0,3 ~ 6 L/min      |
| **Capacidade de carga**      | ≤ 10 mA (DC 5V)    | ≤ 10 mA (DC 5V)    | ≤ 10 mA (DC 5V)    |
| **Temperatura de operação**  | ≤ 80°C             | ≤ 80°C             | ≤ 80°C             |
| **Pressão da água**          | ≤ 1.75 MPa         | ≤ 1.75 MPa         | ≤ 0.8 MPa          |
| **Extensão do fio**          | 16 cm              | 16 cm              | 15 cm              |
| **Diâmetro do sensor**       | 36 mm              | 36 mm              | 34 mm              |
| **Diâmetro da entrada/saída** | 20 mm              | 26 mm              | ~3.3 mm (interior), ~7 mm (exterior) |
| **Dimensões totais (CxLxA)** | 63 x 35 x 36 mm    | 60 x 36 x 34 mm    | 58 x 35 x 27 mm    |
| **Peso**                     | 51 g               | 58 g               | 27 g               |
| **Preço médio**              | R$ 35,00           | R$ 50,00           | R$ 30,00           |


## Projeto de Aplicação
Para integrar o sensor de vazão YF-S201 com o ESP32, pode ser desenvolvido um código que utiliza interrupções para contar os pulsos gerados pelo sensor e calcular a vazão de água em tempo real. Esta aplicação pode ser usada para monitoramento de sistemas hidráulicos via Wi-Fi.

## Justificativa da Escolha do Sensor YF-S201

Para o projeto de monitoramento de caixa d'água, o sensor de vazão **YF-S201 G1/2** foi escolhido por diversos motivos técnicos e logísticos. Dentre os fatores que influenciaram a decisão estão:

1. **Faixa de Vazão Adequada**: O YF-S201 possui uma faixa de medição de 1 a 30 litros por minuto, o que é adequado para o fluxo de água normalmente presente em sistemas domésticos de abastecimento de caixa d'água. Essa faixa é suficiente para monitorar o enchimento e esvaziamento da caixa de maneira eficaz.
   
2. **Compatibilidade com ESP32**: Este sensor é compatível com o microcontrolador **ESP32**, que será utilizado no projeto. A facilidade de integração, com leitura dos pulsos digitais gerados pelo sensor através de interrupções, torna o YF-S201 uma opção prática para o desenvolvimento de sistemas de monitoramento em tempo real.
   
3. **Disponibilidade**: Coincidentemente, um sensor **YF-S201** já estava disponível no laboratório da faculdade. Isso reduziu custos e acelerou o desenvolvimento, já que não foi necessário adquirir um novo componente.

4. **Custo Benefício**: Com um preço médio de **R$ 35,00**, o YF-S201 oferece um bom equilíbrio entre custo e desempenho. Outros sensores comparados, como o **YF-S403** e o **YF-S401**, ou são mais caros, como o YF-S403, ou possuem uma faixa de vazão inadequada para o projeto, como o YF-S401.

Com base nesses fatores, o **YF-S201 G1/2** foi considerado a escolha mais viável e eficiente para o projeto de monitoramento de caixa d'água.

### Referências

ADAFRUIT. **YF-S201 datasheet**. Disponível em: <https://cdn-shop.adafruit.com/product-files/828/C898+datasheet.pdf>. Acesso em: 18 out. 2024.

COMPONENTS 101. **YF-S201 datasheet**. Disponível em: <https://components101.com/sites/default/files/component_datasheet/YF-S201-Datasheet.pdf>. Acesso em: 18 out. 2024.

MAKER HERO. **YF-S201 datasheet**. Disponível em: <https://www.makerhero.com/img/files/download/YF-S201-Datasheet.pdf>. Acesso em: 18 out. 2024.

USINAINFO. **Como o sensor funciona e tipos de sensor de vazão**. Disponível em: <https://www.usinainfo.com.br/blog/sensor-de-fluxo-de-agua-arduino-como-sensor-de-vazao-para-projetos/>. Acesso em: 11 out. 2024.

ELETROGATE. **Funcionamento do sensor YF-S201**. Disponível em: <https://blog.eletrogate.com/sensor-de-fluxo-de-agua/#:~:text=O%20sensor%20de%20fluxo%20de,um%20sinal%20de%20pulso%20correspondente>. Acesso em: 11 out. 2024.
