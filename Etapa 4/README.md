# Resumo do que foi desenvolvido na etapa

## Comunicação WiFi da ESP (Sensores mandando dados para o aplicativo)

A primeira parte desenvolvida nessa etapa foi a implementação da comunicação entre a ESP32 e o backend do aplicativo, permitindo que a ESP enviasse os dados dos sensores de forma eficiente. Utilizando a conectividade Wi-Fi da ESP32, foi integrado o envio de dados coletados dos sensores (como vazão de água, volume total acumulado e distância medida por ultrassônico) para o backend, que é implementado em Python. O código de coleta de dados, previamente funcional, foi adaptado para incluir o envio dessas informações em formato JSON por meio de requisições HTTP POST ao servidor. Isso garante que os dados sejam transmitidos em tempo real, utilizando uma comunicação robusta e compatível com o backend.

Para testar essa funcionalidade, carregamos o novo código na ESP32 e executamos o código do backend em Python. Com as credenciais de Wi-Fi configuradas corretamente, os dados enviados pela ESP começaram a aparecer no terminal onde o backend estava rodando, conforme ilustrado na Figura 1. Além disso, para validar a estabilidade da comunicação Wi-Fi, conectamos a ESP a uma fonte de alimentação independente e observamos que ela continuou transmitindo os dados de forma consistente para o backend. Esse teste confirmou que a comunicação Wi-Fi estava funcionando corretamente e de maneira estável.

Figura 1: Backend recebendo dados no terminal via WiFi.
![teste_wifi](https://github.com/user-attachments/assets/1c2cc8ed-e558-497a-9d10-c9f7d73ad977)
Fonte: Autoria Própria.

Os códigos comentados utilizados para esse teste estão disponíveis [aqui](https://github.com/LauraMWerneck/Projeto_Integrador_3/tree/main/Etapa%204/Teste%20WiFi).

## Criação da Placa
Na análise do esquemático criado na Etapa 3, identificamos soluções mais simples e eficazes para atender aos requisitos do projeto. Adotamos uma fonte de 12V via conector P4, que alimenta tanto a solenóide através do relé quanto um conversor 7805 para fornecer 5V à ESP32 e aos sensores. Também substituímos o módulo de relé por um relé simples, tornando o circuito mais compacto e reduzindo custos sem comprometer a eficiência.

Durante os testes, identificamos instabilidades devido à ausência de capacitores de desacoplamento no 7805, especialmente ao acionar o relé. A adição desses capacitores estabilizou a alimentação. Além disso, o sensor de fluxo apresentou falhas com os 5,05V fornecidos pelo 7805, sendo corrigido com um diodo em série, reduzindo a tensão e melhorando seu desempenho.

Após os ajustes, o circuito revisado mostrou-se mais estável e eficiente. As melhorias foram implementadas diretamente no esquemático, conforme mostra a Figura 2 e no layout da PCB, como mostra a Figura 3, garantindo uma versão pronta para fabricação e montagem.

Figura 2: Novo esquemático do circuito.

![image](https://github.com/user-attachments/assets/5c3e8f1a-b9ca-4e52-bfe0-14bd2a233932)

Fonte: Autoria Própria.

Figura 3: Novo layout da placa.

![image](https://github.com/user-attachments/assets/ef91b98a-1fe3-4cbc-ab22-4aedd2df1495)

Fonte: Autoria Própria.

Após a fabricação da placa, e a instalação dela no sistema físico de teste ela ficou como mostra a Figura 4.

Figura 4: Placa integrando todos os componentes.

![Imagem do WhatsApp de 2025-02-10 à(s) 20 37 38_9340aac4](https://github.com/user-attachments/assets/74f50ccc-80f7-4c33-ab5c-cf762a882bdb)

Fonte: Autoria Própria.

Para mais detalhes das modificações da placa, e para acessar o projeto do Kicad clique [aqui](https://github.com/LauraMWerneck/Projeto_Integrador_3/tree/main/Projeto%20Final/Placa)

## Sistema Físico de Teste
Como visto na Etapa 3, criamos um sistema físico de teste e, nesta última etapa, aprimoramos sua estrutura para acomodar a ESP e a nova placa de forma mais segura e com aparência de um produto final. Para isso, desenvolvemos um suporte impresso em 3D, fixado acima do balde principal, garantindo a estabilidade da ESP e dos sensores durante os testes. O projeto da impressão 3D está ilustrado na Figura 5.

Figura 5: Suporte 3D desenvolvido.

![modelo_3D](https://github.com/user-attachments/assets/b9385b31-8612-4330-ad40-96dacecfa6c8)

Fonte: Autoria Própria.

Após a impressão da peça, e da integração da placa com os sensores o sistema físico de teste ficou como mostra a Figura 4, a Figura 6 e a Figura 7.

Figura 6: Suporte aberto no sistema físico de teste.

![Imagem do WhatsApp de 2025-02-10 à(s) 21 38 06_a600479e](https://github.com/user-attachments/assets/02e8f37c-303b-471d-831d-a688292fd289)

Fonte: Autoria Própria.

Figura 7: Suporte fechado no sistema físico de teste.

![Imagem do WhatsApp de 2025-02-10 à(s) 21 37 33_552d8dbc](https://github.com/user-attachments/assets/edd9a4a1-303a-44e8-9d2d-e9721c0f11af)

Fonte: Autoria Própria.

Para acessar o modelo 3D criado clique [aqui](https://www.tinkercad.com/things/hdSAljJmEcl-pi3?sharecode=l4aGRgi_aN5EzP9HnUlWbnjf8VeXGf09ikW7ILrOMxc)

## Criação das Funcionalidades do Aplicativo

O código do aplicativo app.py utiliza Flask para monitoramento do consumo de água e controle da caixa d'água. Ele recebe e processa dados de sensores, gerencia configurações e fornece informações para um painel em tempo real.

### **Principais Funcionalidades**
- **Recepção de Dados (/ESP_data):** Captura informações dos sensores, como distância, volume e vazão de água. Processa esses dados para calcular o consumo, estimar o tempo de disponibilidade da água e gerar alertas em caso de anomalias, como falta de água.
- **Cadastro de Configurações (/save_data):** Permite que o usuário registre informações como consumo do hidrômetro, custo da água e volume da caixa d’água. Os dados são armazenados para cálculos e análises futuras.
- **Logs em Tempo Real (/logs_stream):** Utiliza Server-Sent Events (SSE) para enviar atualizações contínuas ao frontend, garantindo que os dados exibidos na interface estejam sempre atualizados sem necessidade de recarregamento da página.
- **Leitura de Dados:** O sistema acessa um arquivo local para recuperar configurações e dados históricos do consumo, garantindo continuidade e rastreabilidade das informações.
- **Cálculos:**
  - **Custo por Litro de Água:** Obtido dividindo o custo total da água pelo consumo registrado.
  - **Consumo por Minuto e Hora:** O sistema armazena e exibe a taxa de consumo ao longo do tempo, permitindo uma análise detalhada do uso da água.
  - **Estimativa de Disponibilidade:** Com base na taxa de consumo e no volume atual da caixa d’água, o sistema prevê o tempo restante antes do esgotamento.
  - **Detecção de Falta de Água:** Se os sensores indicam um nível muito baixo, um alerta é gerado para notificar o usuário sobre o problema.

### **Interface Web**
A página HTML fornece uma interface interativa para o monitoramento e controle do consumo de água. Ela inclui:

- **Painel de Monitoramento:**
  - Exibe informações em tempo real sobre consumo, custo e volume disponível.
  - Apresenta alertas visuais sobre possíveis problemas, como baixo nível de água.
- **Gráficos Dinâmicos:**
  - Usa Chart.js para criar gráficos interativos que mostram o consumo de água ao longo do tempo.
  - O usuário pode alternar entre diferentes visualizações, como consumo por minuto, por hora ou por dia.
- **Logs de Alertas:**
  - Registra e exibe eventos importantes, como discrepâncias no consumo e notificações de falta de água.
  - Permite que o usuário acompanhe o histórico de alertas.
- **Formulário de Configuração:**
  - O usuário pode inserir e atualizar dados essenciais, como volume da caixa d’água, custo da água e consumo registrado.
  - Inclui campos para definir metas de consumo e monitorar os custos mensais.
- **Botões Interativos:**
  - Permitem alternar entre diferentes gráficos e logs.
  - Incluem funcionalidades para salvar e enviar novas configurações ao backend.

Os códigos do app.py e da página html podem ser acessados e ter sua documentação detalhada [aquqi](https://github.com/LauraMWerneck/Projeto_Integrador_3/tree/main/Projeto%20Final).

## Teste Final
Com todas as funcionalidades do aplicativo concluídas, a placa integrando os componentes e o sistema físico finalizado, além da comunicação Wi-Fi operando corretamente, chegou o momento de testar o projeto como um todo. O objetivo era garantir seu funcionamento conforme o esperado e verificar se os sensores estavam coletando os dados corretamente.

Assim, ligamos todo o sistema, conectamos os componentes necessários e, visualmente, o projeto com o sistema físico de teste ficou conforme ilustrado na Figura 8.

Figura 8: Protótipo Final.

![Imagem do WhatsApp de 2025-02-10 à(s) 20 39 52_edbd3d94](https://github.com/user-attachments/assets/0bc586c8-47ae-4b7e-8a55-22eb77664c41)

Fonte: Autoria Própria.

Em seguida, inicializamos o sistema e abrimos o aplicativo. Nele, realizamos as configurações necessárias, e logo começou a receber os dados dos sensores e exibi-los para os usuários, conforme ilustrado na Figura 9.

Figura 9: Interface do Aplicativo.

![Imagem do WhatsApp de 2025-02-11 à(s) 21 16 24_23b2c37d](https://github.com/user-attachments/assets/136fc657-4460-4dfa-9cc9-cbe7e1661ed6)

Fonte: Autoria Própria.

# Conclusão do Projeto
O desenvolvimento deste projeto permitiu a integração eficiente de sensores de vazão e volume de água com a ESP32, garantindo a captação e transmissão de dados em tempo real para um aplicativo via Wi-Fi. A implementação bem-sucedida da comunicação entre os sensores e o backend assegurou um monitoramento contínuo e preciso dos níveis de água, proporcionando uma solução funcional para o controle de reservatórios.  

Ao longo das etapas, enfrentamos desafios técnicos como a escolha e calibração dos sensores, a revisão do circuito eletrônico e a estabilidade da comunicação Wi-Fi. A necessidade de ajustes no esquemático da placa e a reorganização dos componentes foram superadas, resultando em uma estrutura mais otimizada e confiável. Além disso, a implementação do backend em Python garantiu uma integração eficiente entre os sensores e o aplicativo, permitindo que os dados fossem processados e exibidos de maneira intuitiva para o usuário.  

O teste final comprovou o funcionamento adequado do sistema, validando a precisão das medições e a estabilidade da transmissão de dados. A interface do aplicativo foi aprimorada para facilitar o uso e a interpretação das informações coletadas. Apesar dos desafios enfrentados, o projeto demonstrou sua viabilidade e abriu caminhos para melhorias, como a otimização da precisão do sensor ultrassônico e a integração de novos recursos, como o controle automatizado da válvula solenoide.  

Com isso, o projeto atinge seu objetivo de oferecer uma solução acessível e eficiente para o monitoramento e controle de água em reservatórios, trazendo benefícios tanto para economia de recursos quanto para a gestão inteligente do consumo hídrico.
