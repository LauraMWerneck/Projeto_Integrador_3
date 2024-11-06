# Descrição de Como o Sistema Físico de Teste Vai Ser Montado

Para este sistema de teste, serão utilizados três componentes principais: um sensor de vazão, uma válvula solenoide e um sensor ultrassônico. A placa ESP atuará como controlador, gerenciando as informações dos sensores e acionando a válvula conforme necessário. 

O sistema físico será composto por uma mangueira transparente conectada ao registro de água. Nessa mangueira, estarão acoplados uma válvula solenóide e o sensor de vazão YF-S201, ambos fixados por uma peça impressa em 3D, projetada para otimizar o desempenho e o controle do fluxo de água. Após o sensor, haverá outra mangueira que levará a água até um balde, representando a caixa d'água. Na parte inferior desse balde, será instalada uma válvula de saída para simular a vazão de água da caixa d'água. 

Um ponto importante é que o balde terá uma tampa, onde será montado o sensor de volume (sensor ultrassônico). Além disso, teremos um segundo balde para escoar a água que sair do balde principal durante os testes de variação de volume.

## Esboço do Sistema de Teste

A figura abaixo representa o esboço do sistema de teste com a disposição dos componentes e a conexão com a ESP. 

**Figura 1**: Esquema do sistema físico de teste.

![Esquema do sistema físico de teste.](https://github.com/LauraMWerneck/Projeto_Integrador_3/blob/main/Etapa%202/Sistema%20F%C3%ADsico%20de%20Teste/sistema_fisico_de_teste.jpg)

Fonte:Autoria própria.

## Para modelagem 3D utilizada no sistema:

A ideia inicial era conectar a válvula solenoide ao sensor de vazão utilizando um conector fêmea-fêmea comum de ½ polegada. No entanto, identificamos uma diferença significativa nos diâmetros internos: 15 mm para a válvula e 11 mm para o sensor. Utilizar um conector de encanamento padrão poderia ampliar ainda mais essa discrepância devido ao espaço interno da peça.

Diante disso, percebemos a importância de minimizar essa diferença abrupta nos diâmetros internos, visando reduzir o risco de cavitação — um fenômeno que gera bolhas de ar nos canos, potencialmente comprometendo a precisão das medições do sensor de vazão.

Para solucionar esse problema, projetamos uma peça personalizada, especificamente modelada para acomodar a variação nos diâmetros internos. A peça foi impressa em 3D, levando em consideração o tamanho total das roscas e os diâmetros internos de cada componente, garantindo uma transição mais suave e eficiente.

![image](https://github.com/user-attachments/assets/097375fc-319b-4a46-adcf-5c576bfcdc11)


## Exemplo de Componentes

**1. Balde:**

JAGUAR UTILIDADES. **Balde com tampa 72L alça plástica industrial**. Disponível em: https://jaguarutilidades.com.br/produto/3014-balde-com-tampa-72l-alca-plastica-industrial/. Acesso em: 30 out. 2024.

**2. Mangueira:**

PADRÃO MANGUEIRAS. **Mangueira plástica cristal**. Disponível em: https://padraomangueiras.com.br/produto/mangueira-plastica-cristal/. Acesso em: 30 out. 2024.

**3. Torneira/Válvula de Saída:**

MULTIFRIO SHOP. **Torneira premium com conector para bebedouro branco/azul**. Disponível em: https://www.multifrioshop.com/pecas-para-bebedouro/torneiras/torneira-premium-com-conector-para-bebedouro-brancoazul. Acesso em: 30 out. 2024.
