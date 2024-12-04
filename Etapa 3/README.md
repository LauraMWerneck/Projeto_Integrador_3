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

As Figura 2, 3 e 4 mostram como ficou o sistema físico montado, os resultados obtidos no teste forma os mesmos do testado sem água, somente o sensor ultrassônico que notamos que ele não calcula tão corretamente a distância da superfície da água, mas isso já está sendo estudado e resolvido.

Figura 2: Sistema físico de teste.

![sistema_fisico_3](https://github.com/user-attachments/assets/2479e922-22b7-4bbb-bf41-c09abdd8e89d)

Fonte: Autoria Própria.

Figura 3: Sistema físico visto por cima.

![sistema_fisico_2](https://github.com/user-attachments/assets/39280e51-157f-4e02-aa28-00d392f19dfa)

Fonte: Autoria Própria.

Figura 4: Sistema físico vista lateral.

![sistema_fisico_1](https://github.com/user-attachments/assets/e24029ef-2fb4-4510-8016-f1ee2530fac0)

Fonte: Autoria Própria.

### Criação do Circuito Completo

Para a criação do circuito completo, consideramos os principais componentes do nosso projeto: os sensores de vazão (YF-S201) e ultrassônico (HC-SR04), além da ESP32 (ESP Wroom 32). Durante o processo, identificamos a necessidade de utilizar um conversor de tensão de 3,3V para 5V, pois o sensor ultrassônico só funcionava corretamente com essa alimentação. Além disso, o sensor de vazão apresentou melhor calibragem e resultados mais precisos quando operando com 5V. Para atender a essa demanda, utilizamos um Módulo Regulador de Tensão Ajustável MT3608 Step Up - 2,5V a 28V, aproveitando um material que já tinhamos disponível e garantindo que fosse adequado às nossas necessidades.

Adicionalmente, pensando na próxima etapa do projeto, incluímos ao circuito uma válvula solenoide. Essa válvula será responsável por controlar o fluxo de água, permitindo ou bloqueando sua passagem conforme necessário para regular o volume no reservatório. Para gerenciar a válvula, percebemos a necessidade de incluir um módulo relé, o qual também já possuíamos. A utilização desse componente irá nos permitir integrar facilmente o controle da válvula ao circuito, otimizando os recursos disponíveis.

Dessa forma, o circuito foi montado ficou como mostrado na Figura 1 e o esquemático desse circuito como mostra a Figura 2.

Figura 5: Esquemático do projeto.

![esquematico](https://github.com/user-attachments/assets/2ca224a2-de12-41d3-b734-978a547af268)

Fonte: Autoria própria.

Neste esquemático, utilizamos bibliotecas prontas para o módulo ESP32 e para o sensor ultrassônico. Entretanto, foi necessário criar os símbolos representativos para os demais componentes do circuito. Assim, desenvolvemos símbolos personalizados para representar os componentes adicionais. 

Para a elaboração da placa com os footprints, foi necessário modificar o esquemático original, uma vez que alguns componentes já possuíam conexões pré-estabelecidas ou não estariam conectados diretamente à placa. Como resultado, o esquemático final da placa ficou conforme ilustrado na Figura 3.

Figura 6: Esquemático da placa.

![esquematico2](https://github.com/user-attachments/assets/93ed7821-b890-4b1f-813c-b48dcecb2a74)

Fonte: Autoria Própria.

Para os *footprints*, utilizamos modelos já existentes para alguns itens, como o sensor de vazão (YF-S201). Em outros casos, foi necessário criar nossos próprios *footprints*, como para o regulador de tensão. O resultado final do circuito da placa que será fabricada, é apresentado na Figura 4.

Figura 7: *Layout* da PCB.

![circuito_placa](https://github.com/user-attachments/assets/f31a5a30-a5b7-43ac-b430-d86836e7125f)

Fonte: Autoria Própria.


## Desenvolvimento do Aplicativo

No aplicativo, a comunicação entre o backend e o frontend foi implementada por meio de uma API, permitindo que o usuário insira os valores necessários, que são salvos e utilizados para cálculos no backend. A próxima etapa do desenvolvimento incluirá a integração para o recebimento dos dados provenientes do microcontrolador, a transmissão dos resultados do backend para o frontend e a criação de uma interface amigável para o usuário.

Confira mais detalhes no repositório: [Projeto Integrador 3 - Aplicativo](https://github.com/LauraMWerneck/Projeto_Integrador_3/tree/main/Etapa%203/Aplicativo)

## Identificação dos Problemas

Durante o desenvolvimento do projeto diversos desafios foram enfrentados e documentados para que pudessem ser adequadamente analisados e resolvidos. Esses problemas estão relacionados tanto ao hardware quanto à implementação e integração dos componentes eletrônicos. A seguir, são detalhados os problemas identificados até o momento:

#### 1. Utilização de Pinos de Strapping na ESP32 WROOM  
Durante a montagem inicial do circuito, foram utilizados os pinos 2 e 5 da ESP32 WROOM, que são pinos críticos para o processo de "strapping". Isso gerou dificuldades ao tentar gravar o código na ESP32, já que o pino 2 é diretamente relacionado ao processo de boot. Como solução temporária, foi adotada a prática de pressionar manualmente o botão de boot durante o envio do código para a placa. No entanto, essa abordagem é pouco prática e pode gerar problemas futuros caso a necessidade de regravação do código seja frequente ou automatizada. Esse problema foi identificado e os pinos serão remanejados para evitar conflitos com as funções de strapping.

#### 2. Má utilização do Visual Studio Code
Durante o desenvolvimento do projeto, enfrentamos dificuldades ao abrir o monitor serial no Visual Studio Code, usado para programar e gravar o código na ESP32. O problema ocorreu devido a erros na organização dos arquivos do projeto e na configuração do sistema de build baseado em CMake. Criamos arquivos de maneira incorreta dentro do projeto, e o arquivo `CMakeLists.txt` não foi ajustado para identificar corretamente o arquivo principal com a função `main`. Isso gerou inconsistências durante a compilação, fazendo com que o código fosse gravado de forma incorreta na ESP32 e impedindo que o monitor serial exibisse as mensagens de saída esperadas. Para resolver, reorganizamos os arquivos respeitando a estrutura padrão do ESP-IDF. Após essa mudança, o sistema passou a compilar corretamente, e o monitor serial voltou a funcionar.

#### 3. Baixa Precisão do Sensor Ultrassônico  
O sensor ultrassônico instalado para medir o volume de água na caixa apresentou limitações de precisão nas leituras. Isso pode comprometer a confiabilidade do sistema de controle, especialmente em situações que demandam maior exatidão nos dados. Já está em andamento a investigação de possíveis melhorias no uso do sensor, como ajustes na sua posição ou alterações no código de processamento dos dados, além da análise de alternativas de sensores que possam substituir o atual.

#### 4. Integração do Sistema e Comunicação com o Aplicativo  
Embora ainda não tenha gerado problemas práticos, a integração dos dados coletados pelos sensores e sua transmissão para o aplicativo via HTML podem ser pontos de atenção. A confiabilidade na comunicação entre a ESP32 e o aplicativo será essencial para o funcionamento do sistema, especialmente em termos de velocidade e consistência na transmissão dos dados.

#### 5. Organização dos Sensores e da Placa de Controle
Outro ponto inportante para termos atenção para a próxima etapa está relacionado à organização física dos sensores, da válvula solenóide e da placa de controle. Como o projeto inclui uma placa principal com os componentes eletrônicos essenciais e conexões externas para os sensores e a válvula, é necessário planejar cuidadosamente a disposição dos cabos, a localização da placa e as medidas de proteção física para garantir a funcionalidade e a durabilidade do sistema.

Esse desafio envolve evitar o emaranhamento dos fios, que pode dificultar a manutenção e gerar interferências elétricas entre os componentes, além de pensar em uma forma de fixar a placa em um local seguro. Também é necessário garantir que a placa e as conexões estejam protegidas contra umidade, respingos de água e outras condições ambientais adversas, utilizando uma caixa ou invólucro adequado. Este problema ainda está em análise para definir a melhor solução, considerando tanto a praticidade quanto os custos envolvidos na implementação de uma organização eficiente e segura.

## Estudo da Viabilidade de Monitorar Vazamentos
O estudo de viabilidade para implementar o monitoramento de vazamentos no projeto de controle da caixa d’água concluiu que a funcionalidade não é viável devido a limitações técnicas e financeiras. O sensor de vazão existente não permite detectar vazamentos na tubulação, e a instalação de sensores adicionais aumentaria os custos e a complexidade. Métodos alternativos, como o uso de dados comparativos com o sensor ultrassônico, são imprecisos e sujeitos a falsos alarmes. Além disso, o ambiente operacional, com baixa pressão e tubulações conectadas em diferentes pontos, dificulta a confiabilidade do sistema.

Dado o alto custo de sensores especializados e a manutenção necessária para evitar falhas, optou-se por não incluir essa funcionalidade no projeto. O foco será para melhorar o controle de enchimento da caixa e a apresentação dos dados no aplicativo, mantendo a solução acessível, eficiente e funcional.

Mais detalhes do que foi levantado nessa pesquisa podem ser acessados nesse [link](https://github.com/LauraMWerneck/Projeto_Integrador_3/tree/main/Etapa%203/Estudo%20da%20Viabilidade%20de%20Monitorar%20Vazamentos)
