# Estudo de Viabilidade do Monitoramento de Vazamentos

Como parte do desenvolvimento do projeto de controle da caixa de água, foi realizado um estudo preliminar para avaliar a 
viabilidade técnica e operacional de incluir um sistema de monitoramento de vazamentos. A proposta consistia em detectar 
vazamentos ao longo da tubulação ou na própria caixa d’água, utilizando os sensores já integrados ao projeto ou componentes 
adicionais. No entanto, após uma análise detalhada, concluiu-se que a implementação dessa funcionalidade não seria viável, pelos 
seguintes motivos:

### 1. Limitações dos Sensores Disponíveis
O sensor de vazão YFS201, utilizado no projeto, mede exclusivamente a quantidade de água que passa pelo fluxo na tubulação principal. 
Para detectar vazamentos, seria necessário instalar sensores adicionais ao longo de toda a tubulação para identificar discrepâncias 
localizadas. Isso aumentaria significativamente a complexidade e o custo do sistema.

### 2. Baixa Precisão no Monitoramento Indireto  
Uma alternativa seria detectar vazamentos de forma indireta, comparando os dados do sensor de vazão com o volume de água registrado 
pelo sensor ultrassônico. Contudo, essa abordagem é limitada pela precisão do sensor ultrassônico, que já apresentou dificuldades para 
medir o volume com exatidão. Pequenas variações ou erros de leitura poderiam ser interpretados como vazamentos falsos.

### 3. Custo Elevado para Implementação  
A instalação de sensores adicionais específicos para monitoramento de vazamentos, como sensores de pressão ou sensores acústicos, 
exigiria um investimento significativo. Isso iria contra o objetivo de manter o projeto acessível e de baixo custo, um dos critérios 
centrais para sua viabilidade.

### 4. Condições Operacionais do Ambiente  
A detecção de vazamentos é especialmente desafiadora em sistemas de abastecimento de água com baixa pressão, tubulações extensas 
ou ramificadas. No ambiente estudado, essas condições tornariam ainda mais complexa a implementação de um sistema confiável de detecção.

### 5. Manutenção e Confiabilidade 
Sensores de vazamento frequentemente requerem manutenção para evitar alarmes falsos causados por fatores externos, como vibrações 
ou variações de pressão. Isso aumentaria a necessidade de intervenções regulares, dificultando a operação prática do sistema.

## Conclusão do Estudo 

Com base nos fatores analisados, conclui-se que a implementação de um sistema de monitoramento de vazamentos não é viável 
dentro do escopo e das limitações técnicas, financeiras e operacionais do projeto. Por essa razão, optou-se por não incluir 
essa funcionalidade no sistema, concentrando os esforços na melhoria dos aspectos centrais do projeto, como o controle de enchimento 
da caixa d’água e a apresentação dos dados no aplicativo. Essa decisão permite manter o foco na entrega de uma solução robusta e 
funcional para o controle eficiente de água.
