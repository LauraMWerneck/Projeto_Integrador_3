## Aplicativo - Etapa 3

  No aplicativo, foi estabelecida a comunicação entre o backend e o frontend por meio de uma API. O usuário insere os valores necessários para os cálculos, organizados em duas áreas principais:  

### Cadastro inicial:
- Inserção do volume de água consumido no mês, conforme indicado na conta de água, em m³.  
- Inserção do valor total gasto com água no mês, em reais.  
  - Essas informações são utilizadas para calcular o custo médio da água na região.  
- Também é solicitado o volume da caixa d'água, em litros.  

### Atualização mensal:
- Inserção do valor da conta de água no mês atual, em reais. 
  - Comparação entre as leituras do hidrômetro e as medições do equipamento desenvolvido.  
- Inserção de uma expectativa de consumo para o próximo mês, em reais.
  - Permitindo estimar o quanto o usuário deve economizar para alcançar seu objetivo.

![image](https://github.com/user-attachments/assets/ba28b97a-dd7a-4782-8fe7-af61d55192bb)

Fonte: Autoria Própria.

### Esses dados são enviados para o backend, onde são armazenados em variáveis para cálculos, são eles: 
- Consumo em reais (por hora, dia, mês e ano).  
- Consumo real (diferença em reais entre o valor do hidrômetro e o equipamento).
- Tempo de água disponível na caixa d'água.

Atualmente, esses dados são exibidos no terminal do VS Code. A proposta é apresentar essas informações diretamente ao usuário por meio do frontend.

![image](https://github.com/user-attachments/assets/199fab65-fb1f-4025-8192-0f77e676c9f2)

Fonte: Autoria Própria.

Ainda estão pendentes algumas funcionalidades descritas na etapa 2 que serão feitas pela etapa 4 pois é necessário a implementação completa de todos os módulos do equipamento. Os próximos passos incluem receber e processar os dados enviados pelo microcontrolador e retornar as informações processadas para a interface do usuário.
