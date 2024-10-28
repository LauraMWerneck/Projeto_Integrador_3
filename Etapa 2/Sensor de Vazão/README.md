
# Sensor de Vazão YF-S201

## Descriçaõ do Sensor
O YF-S201 é um sensor de vazão de água utilizado em projetos eletrônicos e industriais para medir o fluxo de líquidos. É popular devido à sua simplicidade
e baixo custo. Abaixo, detalhamos seu funcionamento, características técnicas e aplicações.

**Figura 1:** Sensor de Vazão YF-S201.

![Sensor de Vazão YF-S201](link)

Fonte: 

### Especificações Técnicas
- **Faixa de Medição de Vazão**: 1 a 30 L/min.
- **Tensão de Operação**: 5 a 18V (comum em 5V para microcontroladores).
- **Corrente Máxima**: 15 mA a 5 V.
- **Conector de Saída**: 3 fios (VCC, GND e sinal de pulso).
- **Temperatura de Operação**: -25°C a 80°C.
- **Pressão Máxima**: 1,75 MPa.
- **Conexão**: Rosca padrão G1/2", adequada para sistemas domésticos e industriais.

### Estrutura e Componentes
O YF-S201 é composto por:
- **Entrada e Saída de Água**: Conexões para tubulação de entrada e saída do líquido.
- **Rotor com Hélice**: Elemento móvel acionado pelo fluxo de água. Cada rotação representa uma quantidade de líquido que passou pelo sensor.
Uma representação do rotor é mostrada na Figura 2.

**Figura 2:** Rotor com Hélice.

![Rotor com Hélice](https://www.usinainfo.com.br/blog/wp-content/uploads/2019/07/IMG_7414.jpg)

Fonte: USINAINFO.
 
- **Sensor de Efeito Hall**: Captura a rotação do rotor, gerando pulsos elétricos a cada volta (ou fração de volta), que são proporcionais à vazão.
Uma representação do sensor de efeito Hall é mostrado na Figura 3.

**Figura 3:** Sensor de Efeito Hall.

![Sensor de Efeito Hall](https://www.usinainfo.com.br/blog/wp-content/uploads/2019/07/IMG_7521mat.jpg)

Fonte: USINAINFO.

### Funcionamento
O YF-S201 mede a vazão de água através de uma turbina interna que gira com o fluxo de líquido. À medida que a água passa pelo sensor, a turbina gira, e o sensor de efeito Hall detecta essas rotações, gerando pulsos elétricos, uma representação desse sistema é mostrado na Figura 4. Cada pulso corresponde a uma quantidade específica de água, que pode ser convertida em uma leitura de vazão por um microcontrolador.

**Figura 4:** Funcionamento do Sensor.

![Funcionamento do Sensor](https://blog.eletrogate.com/wp-content/uploads/2021/03/Principio-do-fluxo-de-agua.gif)

Fonte: ELETROGATE.

Para o YF-S201, são gerados aproximadamente 450 pulsos por litro de água. A fórmula para calcular a vazão em litros por minuto (L/min) baseia-se na contagem dos pulsos durante um intervalo de tempo. Cada pulso gerado pelo sensor equivale a uma vazão de aproximadamente 2,25 mL de água. Portanto, a fórmula básica para calcular a vazão total de água a partir da frequência dos pulsos é:

$Fluxo (L/min)$ = $Frequência dos Pulsos (Hz)/7,5$

Essa fórmula considera que, para cada 7,5 pulsos por segundo (Hz), o fluxo de água é de 1 litro por minuto (L/min).


## Referências

USINAINFO. **Como o sensor funciona e tipos de sensor de vazão**. Disponível em: <https://www.usinainfo.com.br/blog/sensor-de-fluxo-de-agua-arduino-como-sensor-de-vazao-para-projetos/>. Acesso em: 11 out. 2024.

ELETROGATE. **Funcionamento do sensor YF-S201**. Disponível em: <https://blog.eletrogate.com/sensor-de-fluxo-de-agua/#:~:text=O%20sensor%20de%20fluxo%20de,um%20sinal%20de%20pulso%20correspondente>. Acesso em: 11 out. 2024.

