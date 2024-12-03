# Resumo do que foi desenvolvido na Etapa 3

## Testes Individuais dos Sensores

### Sensor de Vazão
Para testar o sensor de vazão (YF-S201), foi desenvolvido um código que recebe os pulsos gerados pelo sensor durante a passagem de água e calcula a vazão com base nesses pulsos e no fator de calibração específico do sensor. O código exibe os resultados do teste, mostrando a vazão em litros por minuto e litros por hora, além de informar o volume total de água que passou pelo sensor desde que o sistema foi iniciado. 

A explicação mais detalhada sobre o teste, juntamente com o código utilizado e sua documentação, está disponível neste [link](https://github.com/LauraMWerneck/Projeto_Integrador_3/blob/main/Etapa%203/Sensor%20de%20Vaz%C3%A3o/README.md).

### Sensor de Volume
Para validar o funcionamento do sensor ultrassônico HC-SR04 no cálculo de volumes de água, foi realizado um teste que avaliou sua precisão em medições de distância. O sistema integrou dados de distância e vazão, ajustando dinamicamente o ponto de referência do sensor conforme o nível de água. Durante o experimento, foram adicionados volumes graduais de água em um balde e comparados os níveis medidos pelo sensor com medições feitas por trena. Os resultados demonstraram que a relação entre o nível e o volume é não linear devido ao formato do recipiente, mas indicaram a viabilidade de criar funções para estimar automaticamente o volume em diferentes recipientes.

O código utilizado no teste, que configura o sensor, realiza medições contínuas e permite ajustes por comandos seriais, está documentado e disponível neste [link](https://github.com/LauraMWerneck/Projeto_Integrador_3/blob/main/Etapa%203/Sensor%20de%20Volume/README.md). O teste concluiu que o sensor ultrassônico é aplicável para medições dinâmicas de volume no projeto, com precisão suficiente para as demandas propostas.

## Integração de Todos os Sensores

Para integrar todos os sensores, começamos planejando o circuito com todos os componentes. Durante essa etapa e durante os testes individuais dos sensores, percebemos a necessidade de adicionar novos elementos, como o conversor de tensão e o módulo relé. Assim, foi elaborado o circuito que inclui não apenas os sensores, mas também a válvula solenóide. A Figura 1 a seguir apresenta o circuito resultante que montamos.

Figura 1: Circuito com os componentes e sensores.
![circuito_componentes](https://github.com/user-attachments/assets/1d959e9f-ad07-4025-9575-14b4a3b50ce9)
Fonte: Autoria Própria.

Este circuito é composto pelo módulo ESP32 (ESP Wroom 32), o sensor de vazão YF-S201, o sensor ultrassônico HC-SR04, uma válvula solenóide, um módulo relé de 5V e um conversor de tensão. A ESP32 alimenta o conversor de tensão, que, por sua vez, fornece energia para os sensores e o módulo relé. A ESP32 é conectada aos sensores por meio de suas saídas de dados. A válvula solenóide e o módulo relé são alimentados por uma fonte de 12V.

É importante ressaltar que para esse primeiro teste de integração de todos os sensores, foi montado um circuito com os componentes principais, sem a inclusão do módulo relé e da válvula solenóide.

### Testes Experimentais

Para a realização dos testes com a integração de todos os sensores, foi desenvolvido um código que combinou tanto a parte do sensor de vazão quanto a do sensor de volume. Entretanto, para os testes dos sensores, foi montado um circuito com os componentes principais, mas sem a inclusão do módulo relé e da válvula solenóide.. A documentação detalhada desse código pode ser acessada através deste [link](https://github.com/LauraMWerneck/Projeto_Integrador_3/blob/main/Etapa%203/Integra%C3%A7%C3%A3o%20dos%20Sensores/README.md), e o código completo está disponível neste outro [link](https://github.com/LauraMWerneck/Projeto_Integrador_3/blob/main/Etapa%203/Integra%C3%A7%C3%A3o%20dos%20Sensores/integracao_sensores.c).

Inicialmente, o circuito e os sensores foram testados sem água, apenas com o circuito montado. No caso do sensor de volume (ultrassônico), foi realizada a medição de distância ao afastar e aproximar a mão da entrada do sensor. Para testar o sensor de vazão, foi simulado o fluxo de água ao assoprar na entrada do sensor, fazendo com que a hélice girasse como se a água estivesse passando. Um vídeo desse teste inicial pode ser visualizado abaixo.

Vídeo 1: Primeiro teste com todos os sensores.

https://github.com/user-attachments/assets/cf840823-a034-4f19-821a-5b99ec565559

Fonte: Autoria Própria.

Foi realizado um segundo teste, desta vez utilizando água. Esse teste considerou o sistema físico que montamos, composto por dois baldes, uma bomba de água e tubulações. O funcionamento do sistema é o seguinte: o balde inferior, cheio de água, alimenta a bomba, que utiliza uma mangueira conectada ao sensor para bombear a água. Após passar pelo sensor, a água é conduzida por outra mangueira e despejada no balde superior. O sensor de volume (ultrassônico) foi posicionado acima do balde superior para medir a distância entre o sensor e a superfície da água.

Vídeo 2: Segundo teste com todos os sensores.



Fonte: Autoria Própria.

### Criação do Circuito Completo

Para a criação do circuito completo, consideramos os principais componentes do nosso projeto: os sensores de vazão (YF-S201) e ultrassônico (HC-SR04), além da ESP32 (ESP Wroom 32). Durante o processo, identificamos a necessidade de utilizar um conversor de tensão de 3,3V para 5V, pois o sensor ultrassônico só funcionava corretamente com essa alimentação. Além disso, o sensor de vazão apresentou melhor calibragem e resultados mais precisos quando operando com 5V. Para atender a essa demanda, utilizamos um Módulo Regulador de Tensão Ajustável MT3608 Step Up - 2,5V a 28V, aproveitando um material que já tinhamos disponível e garantindo que fosse adequado às nossas necessidades.

Adicionalmente, pensando na próxima etapa do projeto, incluímos ao circuito uma válvula solenoide. Essa válvula será responsável por controlar o fluxo de água, permitindo ou bloqueando sua passagem conforme necessário para regular o volume no reservatório. Para gerenciar a válvula, percebemos a necessidade de incluir um módulo relé, o qual também já possuíamos. A utilização desse componente irá nos permitir integrar facilmente o controle da válvula ao circuito, otimizando os recursos disponíveis.

Dessa forma, o circuito foi montado ficou como mostrado na Figura 1 e o esquemático desse circuito como mostra a Figura 2.

Figura 2: Esquemático do projeto.

![esquematico](https://github.com/user-attachments/assets/2ca224a2-de12-41d3-b734-978a547af268)

Fonte: Autoria própria.

Neste esquemático, utilizamos bibliotecas prontas para o módulo ESP32 e para o sensor ultrassônico. Entretanto, foi necessário criar os símbolos representativos para os demais componentes do circuito. Assim, desenvolvemos símbolos personalizados para representar os componentes adicionais. 

Para a elaboração da placa com os footprints, foi necessário modificar o esquemático original, uma vez que alguns componentes já possuíam conexões pré-estabelecidas ou não estariam conectados diretamente à placa. Como resultado, o esquemático final da placa ficou conforme ilustrado na Figura 3.

Figura 3: Esquemático da placa.

![esquematico2](https://github.com/user-attachments/assets/93ed7821-b890-4b1f-813c-b48dcecb2a74)

Fonte: Autoria Própria.

Para os *footprints*, utilizamos modelos já existentes para alguns itens, como o sensor de vazão (YF-S201). Em outros casos, foi necessário criar nossos próprios *footprints*, como para o regulador de tensão. O resultado final do circuito da placa que será fabricada, é apresentado na Figura 4.

Figura 4: *Layout* da PCB.

![circuito_placa](https://github.com/user-attachments/assets/f31a5a30-a5b7-43ac-b430-d86836e7125f)

Fonte: Autoria Própria.


## Desenvolvimento do Aplicativo

## Identificação dos Problemas

## Estudo da Viabilidade de Monitorar Vazamentos
O estudo de viabilidade para implementar o monitoramento de vazamentos no projeto de controle da caixa d’água concluiu que a funcionalidade não é viável devido a limitações técnicas e financeiras. O sensor de vazão existente não permite detectar vazamentos na tubulação, e a instalação de sensores adicionais aumentaria os custos e a complexidade. Métodos alternativos, como o uso de dados comparativos com o sensor ultrassônico, são imprecisos e sujeitos a falsos alarmes. Além disso, o ambiente operacional, com baixa pressão e tubulações conectadas em diferentes pontos, dificulta a confiabilidade do sistema.

Dado o alto custo de sensores especializados e a manutenção necessária para evitar falhas, optou-se por não incluir essa funcionalidade no projeto. O foco será para melhorar o controle de enchimento da caixa e a apresentação dos dados no aplicativo, mantendo a solução acessível, eficiente e funcional.

Mais detalhes do que foi levantado nessa pesquisa podem ser acessados nesse [link](https://github.com/LauraMWerneck/Projeto_Integrador_3/tree/main/Etapa%203/Estudo%20da%20Viabilidade%20de%20Monitorar%20Vazamentos)
