# Resumo do que foi desenvolvido na etapa

## Comunicação WiFi da ESP (Sensores mandando dados para o aplicativo)

A primeira parte desenvolvida nessa etapa foi a implementação da comunicação entre a ESP32 e o backend do aplicativo, permitindo que a ESP enviasse os dados dos sensores de forma eficiente. Utilizando a conectividade Wi-Fi da ESP32, foi integrado o envio de dados coletados dos sensores (como vazão de água, volume total acumulado e distância medida por ultrassônico) para o backend, que é implementado em Python. O código de coleta de dados, previamente funcional, foi adaptado para incluir o envio dessas informações em formato JSON por meio de requisições HTTP POST ao servidor. Isso garante que os dados sejam transmitidos em tempo real, utilizando uma comunicação robusta e compatível com o backend.

Para testar essa funcionalidade, carregamos o novo código na ESP32 e executamos o código do backend em Python. Com as credenciais de Wi-Fi configuradas corretamente, os dados enviados pela ESP começaram a aparecer no terminal onde o backend estava rodando, conforme ilustrado na Figura 1. Além disso, para validar a estabilidade da comunicação Wi-Fi, conectamos a ESP a uma fonte de alimentação independente e observamos que ela continuou transmitindo os dados de forma consistente para o backend. Esse teste confirmou que a comunicação Wi-Fi estava funcionando corretamente e de maneira estável.

Figura 1: Backend recebendo dados no terminal via WiFi.
![teste_wifi](https://github.com/user-attachments/assets/1c2cc8ed-e558-497a-9d10-c9f7d73ad977)
Fonte: Autoria Própria.

Os códigos comentados utilizados para esse teste estão disponíveis [aqui](https://github.com/LauraMWerneck/Projeto_Integrador_3/tree/main/Etapa%204/Teste%20WiFi).

## Criação da Placa
Na etapa 3, desenvolvemos o esquemático e o layout de uma placa para integrar todas as partes do projeto. Contudo, foi necessário revisar tanto o esquemático quanto o posicionamento dos componentes na placa. Essa revisão foi motivada pela adição de novos componentes e a substituição de alguns elementos existentes, com o objetivo de otimizar o projeto. O esquemático revisado e o novo layout final estão representados nas figuras 2 e 3.

Figura 2: Novo esquemático do circuito.
![esquematico](https://github.com/user-attachments/assets/4e87906f-9657-4ffa-9927-5bbc4826d271)
Fonte: Autoria Própria.

Figura 3: Nova placa.
![visualizacao_3D](https://github.com/user-attachments/assets/46564992-8339-48fd-8922-ab275b5f9313)
Fonte: Autoria Própria.



Sensores coletando corretamente
Criação das funcionalidades do aplicativo
Resolução dos problemas encontrados
Parte mecânica completa 


# Conclusão do Projeto
