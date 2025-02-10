# Desenvolvimento da PCI

## Problemas encontrados na etapa anterior

Analisando a placa anterior, identificamos soluções mais simples e eficazes para atender aos requisitos do projeto. A alimentação foi repensada, adotando uma fonte de 12V conectada via P4, capaz de alimentar tanto a solenóide de 12V através do relé quanto um conversor 7805, que fornece 5V para a ESP32 e os sensores, garantindo seu funcionamento adequado. Além disso, substituímos o módulo de relé por um relé simples, resultando em uma construção mais compacta, reduzindo a complexidade e os custos sem comprometer a eficiência do sistema.

Figura 1: Esquemático do projeto.

![image](https://github.com/user-attachments/assets/5c3e8f1a-b9ca-4e52-bfe0-14bd2a233932)

## Fase de Testes

Durante a fase de testes, identificamos alguns problemas relacionados à estabilidade do circuito. Inicialmente, o 7805 foi utilizado sem capacitores de desacoplamento, o que resultou em instabilidades no funcionamento do sistema, especialmente ao acionar o relé com a válvula solenóide conectada. Para resolver esse problema, adicionamos capacitores de desacoplamento ao circuito, garantindo uma alimentação mais estável.

Figura 2: Capacitores de desacoplamento.

![image](https://github.com/user-attachments/assets/ebc300a5-801a-4ce4-b471-411639809fa4)

Outro problema identificado foi a instabilidade do sensor de fluxo quando operando com os 5,05V fornecidos pelo 7805. Para corrigir essa questão, inserimos um diodo em série, reduzindo a tensão de alimentação do sensor para aproximadamente 4,7V, o que melhorou significativamente seu desempenho.

Figura 3: Diodo redutor de tensão.

![image](https://github.com/user-attachments/assets/556d0634-686c-4f19-849d-f67a66424c8a)



## Layout e 3D

Com as correções apresentadas anteriormente, o circuito revisado apresentou um funcionamento mais estável e eficiente. As alterações foram implementadas diretamente no esquemático e no layout da PCB, garantindo que a nova versão esteja adequada para fabricação e montagem.

Figura 4: Layout PCB.

![image](https://github.com/user-attachments/assets/ef91b98a-1fe3-4cbc-ab22-4aedd2df1495)


Figura 5: Visualização 3D.

![image](https://github.com/user-attachments/assets/a708c9c7-5ae6-4e70-b2d6-c8063bc69c3f)



## Lista de Componentes

1x Conector p4

1x Barra pino femea

1x Barra pino macho

2x diodo 1N4007

1x Conector KRE 2 pinos

1x Capacitor 0.33uF

1x Capacitor 0.1uF

1x 7805

1x Relé 5V SRD-05VDC-SL-C

1x Dissipador TO-220

## Placa montada final

