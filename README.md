# 📦 Projeto Integrador 3 - Controle Automático de Caixa d'Água

## 🔍 Visão Geral

O **Projeto Integrador 3** tem como objetivo o desenvolvimento de um sistema inteligente para o controle automatizado de uma caixa d'água. O sistema foi projetado para monitorar e gerenciar o nível de água na caixa utilizando sensores e tecnologia de comunicação sem fio (Wi-Fi). A ESP32 é a placa responsável pela coleta dos dados e pela comunicação com o backend, enquanto o aplicativo web proporciona uma interface visual para o usuário.

### Funcionalidades Principais:
- **Monitoramento de Nível de Água:** O sensor ultrassônico HC-SR04 é utilizado para medir a distância da superfície da água, estimando seu nível e volume na caixa d'água.
- **Controle de Vazão:** O sensor de vazão YF-S201 é utilizado para monitorar a quantidade de água consumida e o fluxo de água na caixa.
- **Integração com a Internet:** A ESP32 utiliza Wi-Fi para enviar os dados coletados para um backend em Python, o qual armazena e processa as informações.
- **Exibição no Aplicativo:** O aplicativo web mostra os dados de vazão e nível de água em tempo real, permitindo que o usuário monitore a caixa d'água de forma intuitiva.
- **Controle da Válvula Solenóide:** O sistema inclui uma válvula solenóide controlada por um módulo relé, que permite desligar ou ligar o fluxo de água, dependendo dos dados de nível.

## 🚀 Como Funciona

### 1. **Sensores**
   O sistema conta com dois sensores principais:
   - **Sensor de Vazão (YF-S201):** Mede a quantidade de água que passa por um tubo, enviando pulsos à ESP32. A partir desses pulsos, a ESP32 calcula a vazão de água (litros por minuto) e o volume total consumido.
   - **Sensor Ultrassônico (HC-SR04):** Mede a distância entre o sensor e a superfície da água, permitindo calcular o nível de água na caixa. Isso é feito utilizando o tempo de retorno de um sinal ultrassônico.

### 2. **Placa e Circuito**
   A ESP32 é a central de processamento do sistema. Ela recebe os dados dos sensores, processa as informações e envia esses dados para o backend via Wi-Fi. O circuito inclui:
   - **Conversor de Tensão:** Para fornecer 5V aos sensores que exigem essa tensão de alimentação.
   - **Módulo Relé:** Controla a válvula solenóide para permitir o controle do fluxo de água.

### 3. **Backend**
   O backend é implementado em **Python** e recebe os dados enviados pela ESP32 através de requisições HTTP POST. Os dados são processados e armazenados, permitindo consultas e análises do comportamento do sistema.

### 4. **Aplicativo Web**
   O aplicativo web é a interface onde os dados são exibidos para o usuário. Ele mostra informações em tempo real sobre:
   - Nível de água na caixa.
   - Vazão de água e volume consumido.
   
   O backend envia as informações em formato JSON para o frontend (aplicativo web), permitindo a atualização automática e em tempo real da interface.

## 📂 Estrutura do Repositório

```
📦 Projeto_Integrador_3  
 ┣ 📂 Etapa 1/              # Documentação do que foi desenvolvido na etapa 1  
 ┣ 📂 Etapa 2/              # Documentação do que foi desenvolvido na etapa 2  
 ┣ 📂 Etapa 3/              # Documentação do que foi desenvolvido na etapa 3  
 ┣ 📂 Etapa 4/              # Documentação do que foi desenvolvido na etapa 4  
 ┣ 📂 Projeto Final/        # Pasta com os códigos e esquemáticos finais  
     ┣ 📄 main.c            # Código da ESP32  
     ┣ 📄 app.py            # Código do servidor em Python  
     ┣ 📄 index.html        # Aplicativo para visualização dos dados  
     ┣ 📂 Placa/            # Esquemáticos e layout da PCB  
 ┣ 📜 README.md             # Documentação principal  
 ┣ 📜 README_1.md           # Primeiro README.md feito com o resumo do objetivo do projeto  
```

## 💻 Requisitos

Para rodar o projeto, é necessário ter os seguintes componentes e softwares:

### Hardware:
- **ESP32 (ESP-WROOM-32)** – Microcontrolador responsável pelo processamento dos dados.
- **Sensor Ultrassônico HC-SR04** – Para medição do nível de água.
- **Sensor de Vazão YF-S201** – Para medir o fluxo de água.
- **Válvula Solenóide e Módulo Relé** – Para controlar o fluxo de água.
- **Conversor de Tensão** – Para alimentar os sensores.

### Software:
- **Python 3.x** – Para rodar o backend do servidor.
- **Bibliotecas ESP32** – Para programar a ESP32.
- **HTML/CSS/JavaScript** – Para o desenvolvimento da interface do aplicativo web.

## ⚙️ Como Rodar

### 1. **Configuração da ESP32:**
   - Baixe o código da ESP32 (main.c) e configure a placa utilizando o ESP-IDF do Visual Studio Code.
   - Conecte os sensores de vazão e ultrassônicos aos pinos apropriados na ESP32.
   - Configure a conexão Wi-Fi com as credenciais da sua rede.

### 2. **Configuração do Backend:**
   - Clone o repositório e instale as dependências necessárias para rodar o servidor em Python.
   - Execute o código Python (`app.py`) para iniciar o backend.
   - O backend estará escutando as requisições HTTP POST enviadas pela ESP32.

### 3. **Interface Web:**
   - Abra o arquivo `index.html` em um navegador para acessar a interface do aplicativo.
   - O frontend vai se conectar automaticamente ao backend para visualizar os dados em tempo real.

### 4. **Testes e Monitoramento:**
   - Teste o sistema monitorando os dados de vazão e nível de água, além de verificar o controle da válvula solenóide através da interface web.



