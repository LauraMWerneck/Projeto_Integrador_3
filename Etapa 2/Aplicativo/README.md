# Fórmulas matemáticas do aplicativo

### O microcontrolador irá retornar os seguintes valores para o backend do aplicativo:

![image](https://github.com/user-attachments/assets/d58d1870-fbc9-4889-a9d1-eb82c1c3cce9)

### O usuário insere os seguintes valores através da conta de água: 

![image](https://github.com/user-attachments/assets/58768251-213b-471a-8c43-fec901259b3a)

Assim conseguimos saber o custo da água na região que o usuário irá utilizar o produto.

## Áreas do aplicativo e seus devidos cálculos

### Consumo em Reais (ajustado de acordo com a hora e data):

![image](https://github.com/user-attachments/assets/89f6a925-cd30-49ac-9220-e7105e1dd0bf)

### Água disponível na caixa d’água:

![image](https://github.com/user-attachments/assets/ca851b3a-1e3e-45a4-a8bb-efb8784f788b)

### Consumo real (diferença em reais com o valor do Hidrômetro):

![image](https://github.com/user-attachments/assets/b8a04943-1d4a-45bf-877b-a129193f8f00)

### Caso acabe a água, tempo de água disponível:

Cálculo feito no consumo normal com base no consumo dos últimos 3 dias: 

![image](https://github.com/user-attachments/assets/ab2bee7b-d548-496c-ad13-2f1c104d80b2)

### Expectativa de consumo para próximo mês (disponível apenas depois do primeiro mês de uso): 

![image](https://github.com/user-attachments/assets/02ceb5bc-57dc-4ad9-a358-1a9b88c30ce2)

Esse erro é baseado nos gastos de água da cidade durante o ano, ou nos últimos 6 meses do usuário, ou o mais confiável nos últimos 12 meses do usuário.

### Quanto você gostaria de gastar no próximo mês? (disponível apenas depois do primeiro mês de uso): 

![image](https://github.com/user-attachments/assets/f724b8ec-641f-46f3-b8df-c8c98ba20881)

### Limitar aviso (notificar excesso de gasto) e próxima manutenção (Notificar dia da próxima manutenção) não precisam de fórmulas.
