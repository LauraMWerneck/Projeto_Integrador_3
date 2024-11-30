# Resumo do que foi desenvolvido na Etapa 3

## Testes Individuais dos Sensores

### Sensor de Vazão
Para testar o sensor de vazão (YF-S201), foi desenvolvido um código que recebe os pulsos gerados pelo sensor durante a passagem de água e calcula a vazão com base nesses pulsos e no fator de calibração específico do sensor. O código exibe os resultados do teste, mostrando a vazão em litros por minuto e litros por hora, além de informar o volume total de água que passou pelo sensor desde que o sistema foi iniciado. 

A explicação mais detalhada sobre o teste, juntamente com o código utilizado e sua documentação, está disponível neste [link](https://github.com/LauraMWerneck/Projeto_Integrador_3/blob/main/Etapa%203/Sensor%20de%20Vaz%C3%A3o/README.md).

### Sensor de Volume


## Integração de Todos os Sensores

Para integrar todos os sensores, começamos planejando o circuito com todos os componentes. Durante essa etapa e durante os testes individuais dos sensores, percebemos a necessidade de adicionar novos elementos, como o conversor de tensão e o módulo relé. Assim, foi elaborado o circuito que inclui não apenas os sensores, mas também a válvula solenóide. A Figura 1 a seguir apresenta o circuito resultante que montamos.

Figura 1: Circuito com os componentes e sensores.
![circuito_componentes](https://github.com/user-attachments/assets/1d959e9f-ad07-4025-9575-14b4a3b50ce9)
Fonte: Autoria Própria.

Este circuito é composto pelo módulo ESP32 (ESP Wroom 32), o sensor de vazão YF-S201, o sensor ultrassônico HC-SR04, uma válvula solenóide, um módulo relé de 5V e um conversor de tensão. A ESP32 alimenta o conversor de tensão, que, por sua vez, fornece energia para os sensores e o módulo relé. A ESP32 é conectada aos sensores por meio de suas saídas de dados. A válvula solenóide e o módulo relé são alimentados por uma fonte de 12V.

Para os testes dos sensores, inicialmente, foi montado um circuito com os componentes principais, mas sem a inclusão do módulo relé e da válvula solenóide.

### Testes Experimentais


### Criação do Circuito Completo

## Desenvolvimento do Aplicativo

## Identificação dos Problemas

## Estudo da Viabilidade de Monitorar Vazamentos
