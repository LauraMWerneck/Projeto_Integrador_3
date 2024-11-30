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

Dessa forma, o circuito foi montado como mostra a Figura 2.

Figura 2: Esquemático do projeto.

![esquematico](https://github.com/user-attachments/assets/2ca224a2-de12-41d3-b734-978a547af268)

Fonte: Autoria própria.

Neste esquemático, utilizamos bibliotecas prontas para o módulo ESP32 e para o sensor ultrassônico. Entretanto, foi necessário criar os símbolos representativos para os demais componentes do circuito. Assim, desenvolvemos símbolos personalizados para representar os componentes adicionais. 

Para os *footprints*, utilizamos modelos já existentes para alguns itens, como o sensor de vazão (YF-S201). Em outros casos, foi necessário criar nossos próprios *footprints*, como para o regulador de tensão. O resultado final, incluindo o *footprint* da placa que será fabricada, é apresentado na Figura 3.

Figura 3: *Footprint* do circuito.


Fonte: Autoria Própria.


## Desenvolvimento do Aplicativo

## Identificação dos Problemas

## Estudo da Viabilidade de Monitorar Vazamentos
