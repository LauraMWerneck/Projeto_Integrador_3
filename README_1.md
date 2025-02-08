# Projeto Integrador III - Monitoramento de Consumo de Água

Este projeto visa desenvolver um sistema completo para monitoramento e controle do consumo de água em caixas d'água. Utilizando sensores de vazão e volume, o sistema fornecerá dados sobre a quantidade de água disponível e utilizada, permitindo ao usuário gerenciar melhor seus recursos hídricos.

## Objetivo

O objetivo principal é criar um dispositivo capaz de:
- Monitorar o volume de água disponível na caixa d'água.
- Medir a vazão de água que entra no sistema.
- Fornecer informações sobre o consumo de água ao longo do tempo (diário, semanal e mensal).
- Avisar o usuário sobre a necessidade de manutenção e limpeza da caixa d'água.
- Estimar o tempo restante de água disponível em caso de falta de abastecimento, com base nos dados de consumo anteriores.

## Funcionalidades

- **Sensores**:
  - **Sensor de Vazão**: Mede o fluxo de água que entra na caixa d'água, permitindo identificar possíveis interrupções no abastecimento ou desperdícios.
  - **Sensor de Volume**: Mede o nível de água presente na caixa d'água, garantindo o acompanhamento contínuo do volume disponível.
  
- **Controle de Consumo**: Os dados são integrados a um aplicativo, onde o usuário poderá visualizar seu consumo de água em diferentes períodos (diário, semanal, mensal), e comparar com os dados do hidrômetro.

- **Estimativa de Consumo**: Em casos de falta de água, o sistema estima quanto tempo a água restante na caixa irá durar, com base no consumo médio anterior.

- **Notificações de Manutenção**: Com base no tempo de uso e nos dados de consumo, o sistema pode alertar o usuário sobre a necessidade de limpeza ou manutenção da caixa d'água.

## Componentes do Sistema

- **Microcontrolador**: Responsável pela coleta e processamento dos dados dos sensores.
- **Sensores de Vazão e Volume**: Para monitoramento da entrada de água e volume na caixa d'água.
- **Aplicativo**: Interface para o usuário acompanhar o consumo e obter notificações.

## Uso

O usuário poderá instalar o equipamento na entrada de sua caixa d'água, conectando os sensores ao sistema. Através do aplicativo, ele poderá acompanhar o consumo de água em tempo real, sendo informado sobre possíveis problemas (falta d'água, necessidade de manutenção) e tomando decisões com base nos dados fornecidos.
