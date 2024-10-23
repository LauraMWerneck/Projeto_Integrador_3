# Resumo do que foi desenvolvido na Etapa 1

Nesta etapa do projeto, foi realizada uma pesquisa detalhada sobre os componentes necessários e o desenvolvimento de um aplicativo 
para monitorar e controlar um sistema hidráulico utilizando um microcontrolador. A pesquisa abordou tanto os aspectos de hardware 
quanto de software, além da escolha de novos componentes como válvulas solenoides e relés que serão necessários para o funcionamento 
completo do sistema.

## Microcontrolador Selecionado

O microcontrolador escolhido foi o ESP32 WROOM, devido ao seu custo-benefício e sua capacidade de atender aos requisitos do projeto, 
como conectividade Wi-Fi e compatibilidade com diversos sensores. Além disso, o ESP32 oferece uma solução mais barata e eficiente em 
comparação com a Raspberry Pi Pico W, sem comprometer o desempenho necessário para o projeto.

## Desenvolvimento do Aplicativo

O desenvolvimento do aplicativo foi pensado para integrar um microcontrolador ESP com um backend em Python e um frontend em HTML.
A escolha por Python no backend se deu por sua facilidade de uso e sua vasta biblioteca de suporte para comunicação com microcontroladores,
especialmente no recebimento e processamento de dados em tempo real.

O frontend em HTML já está parcialmente desenvolvido e oferece uma interface amigável para que os usuários possam monitorar e controlar o 
sistema. A integração completa com o backend será realizada após os testes com o ESP32, assegurando que a comunicação e o desempenho do 
hardware sejam validados antes de avançar com a lógica do backend.

## Componentes Pesquisados

### Sensor de Vazão - YF-S201

O sensor de vazão YF-S201 foi escolhido após uma análise de diversos modelos. Este sensor é capaz de medir o fluxo de água entre
1 a 30 litros por minuto e é compatível com o ESP32, operando a 5V. A integração será realizada através de leitura de pulsos digitais
gerados pelo sensor, que serão convertidos em leituras de vazão pelo microcontrolador.

**Especificações do YF-S201:**
- Faixa de Medição: 1 a 30 L/min
- Tensão de Operação: 5 a 18V DC
- Compatibilidade: ESP32 (3.3V nos pinos digitais)
- Custo: R$ 35,00

**Justificativa da Escolha:**
- **Compatibilidade com ESP32:** Fácil integração com leitura de pulsos digitais.
- **Faixa de Vazão:** Adequada para sistemas domésticos de abastecimento.
- **Custo Benefício:** Preço acessível e disponibilidade no laboratório.

### Sensor de Nível de Água - HC-SR04

Para a medição de nível de água, foi selecionado o sensor ultrassônico HC-SR04, que oferece uma medição linear com alta precisão,
embora não seja à prova d'água. Sua faixa de medição vai de 2 cm a 4 metros, sendo ideal para monitoramento de níveis em caixas d'água
de pequeno e médio porte.

**Especificações do HC-SR04:**
- Faixa de Medição: 2 cm a 4 metros
- Precisão: 3 mm
- Custo: Aproximadamente R$ 8,00

### Novos Componentes Adicionados

Durante as pesquisas, identificamos a necessidade de novos componentes para o sistema:
- **Válvula Solenoide:** Para controle automatizado do fluxo de água.
- **Relés:** Para ativar ou desativar a válvula e outros dispositivos elétricos do sistema.

Esses componentes serão integrados ao projeto para garantir o controle preciso do sistema hidráulico.
