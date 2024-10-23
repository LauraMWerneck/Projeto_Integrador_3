# Escolha do Sensor de Volume

Para a medição de nível da água em uma caixa d'água, é essencial utilizar um sensor que forneça leituras lineares e precisas. Isso garante que os dados obtidos sejam confiáveis para as análises necessárias. A seguir, apresentamos algumas opções de sensores utilizados para medir o nível da água que encontramos em nossas pesquisas:

### 1. Sensor do tipo boia:
Este tipo de sensor funciona como uma chave de limite (on-off), ou seja, ele apenas indica quando a água atinge um nível específico. Portanto, ele não oferece uma medição contínua ou analógica, o que impede a obtenção de dados com boa resolução. Mesmo que vários sensores de boia sejam utilizados em conjunto, eles não conseguem fornecer a precisão necessária para medições mais detalhadas.

[Exemplo](https://www.fermarc.com/produto/sensor-de-nivel-de-agua.html#:~:text=O%20sensor%20de%20n%C3%ADvel%20de,desloca%20um%20pouco%20o%20flutuador)  

### 2. Sensor ultrassônico:
Este sensor mede a distância entre o sensor e a superfície da água através da emissão de ondas ultrassônicas. O modelo HC-SR04, por exemplo, consegue medir até 4 metros com uma precisão de aproximadamente 3 mm, oferecendo uma medição linear. No entanto, uma das suas limitações é o ângulo de abertura de cerca de 15 graus, que pode gerar leituras imprecisas se houver bordas ou obstáculos próximos na caixa d'água. Além disso, o HC-SR04 não é à prova d'água, o que limita sua robustez em ambientes com alta umidade. Seu baixo custo (aproximadamente 8 reais por unidade) faz dele uma opção interessante para projetos de pequeno porte.

[Exemplo](https://www.robocore.net/sensor-robo/sensor-de-distancia-ultrassonico-hc-sr04?gad_source=1&gclid=CjwKCAjw1NK4BhAwEiwAVUHPUM2qHLxETvUIdYOGJupQ2GE1Csmj0hMyS9Otl42UBp8TCn5XkkAFlRoC4wsQAvD_BwE)  

### 3. Sensor potenciométrico:
Similar aos sensores de nível de combustível de veículos, este sensor consiste em uma boia conectada a um potenciômetro angular. Conforme a boia sobe ou desce com o nível da água, o potenciômetro gera um sinal elétrico proporcional à altura da água, permitindo medições lineares. Embora esse sistema seja robusto e confiável, o custo médio (cerca de 120 reais) pode ser considerado elevado, e a aplicabilidade pode ser limitada devido à grande variedade de formatos e tamanhos de caixas d'água.

[Exemplo](https://produto.mercadolivre.com.br/MLB-1344418581-sensor-nivel-boia-bosch-civic-18-20-2012-2013-2014-2015-_JM#position%3D3%26search_layout%3Dstack%26type%3Ditem%26tracking_id%3Dc3022dd1-b3b7-4062-82dc-22f2bc8ecaa4)  

### Considerações finais:
Levando em consideração os requisitos de custo e versatilidade do projeto, o sensor ultrassônico HC-SR04 foi considerado a opção mais adequada. 

### Especificações técnicas do HC-SR04:
- **Tensão de operação**: 5V
- **Corrente de operação**: < 15mA
- **Ângulo de medição**: Aproximadamente 15 graus
- **Faixa de medição**: 2 cm a 4 metros
- **Precisão**: Aproximadamente 3 mm
- **Frequência do ultrassom**: 40 kHz

### Componentes do HC-SR04:
- **Pino Trigger**: Responsável pela emissão do pulso ultrassônico.
- **Pino Echo**: Recebe o sinal refletido e calcula o tempo de retorno.
- **Dois transdutores ultrassônicos**: Um atua como transmissor e o outro como receptor.

### Limitações:
- **Ângulo de abertura**: O campo de visão de 15 graus pode gerar interferência com objetos laterais.
- **Não é à prova d'água**: Não recomendado para ambientes com alta umidade, a menos que seja protegido adequadamente.

### Cálculo da distância:
A distância entre o sensor e a superfície da água é calculada com base no tempo de retorno do pulso ultrassônico. O cálculo é feito pela fórmula:

**Distância = (Velocidade do som × Tempo de retorno) / 2**

A velocidade do som no ar é de aproximadamente 340 m/s. O fator de divisão por dois se deve ao fato de que o som percorre a distância de ida e volta entre o sensor e a superfície da água.

O sensor ultrassônico HC-SR04 destaca-se pela sua simplicidade de implementação e custo acessível, tornando-o uma solução eficaz para medição de nível de água em caixas d'água de pequeno a médio porte.

### Simulação do sensor ultrassônico HC-SR04:
Utilizando o site TinkerCAD, foi possivel fazer uma simulação inicial do sensor, o qual apresenta a distancia do objeto no monitor serial:
![image](https://github.com/user-attachments/assets/ccdfcfde-f5be-4639-b049-a577a22a9823)

Abaixo está o código de exemplo para a simulação do sensor HC-SR04 usado no TinkerCAD. Esse código mede a distância até o objeto mais próximo e exibe o resultado tanto em centímetros quanto em polegadas.

```cpp
// C++ code
/*
  Ping))) Sensor

  Este código lê um sensor ultrassônico Ping))) 
  e retorna a distância até o objeto mais próximo. 
  Para isso, ele envia um pulso ao sensor para iniciar uma leitura 
  e, em seguida, ouve o retorno do pulso. O comprimento do pulso retornado 
  é proporcional à distância do objeto ao sensor.

  Circuito:
   * Conexão +V do sensor PING))) ligada ao +5V
   * Conexão GND ligada ao terra
   * Conexão SIG ligada ao pino digital 7

  Mais detalhes: http://www.arduino.cc/en/Tutorial/Ping

  Este código de exemplo está em domínio público.
*/

int inches = 0;
int cm = 0;

long readUltrasonicDistance(int triggerPin, int echoPin)
{
  pinMode(triggerPin, OUTPUT);  // Limpa o pino trigger
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);
  // Define o pino trigger em estado ALTO por 10 microssegundos
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);
  pinMode(echoPin, INPUT);
  // Lê o pino de eco e retorna o tempo de viagem da onda sonora em microssegundos
  return pulseIn(echoPin, HIGH);
}

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  // Mede o tempo de ping em cm
  cm = 0.01723 * readUltrasonicDistance(7, 7);
  // Converte para polegadas dividindo por 2.54
  inches = (cm / 2.54);
  Serial.print(inches);
  Serial.print("in, ");
  Serial.print(cm);
  Serial.println("cm");
  delay(100); // Aguarda 100 milissegundos
}
```
### Referências:
JAVATPOINT. **IoT Project using Ultrasonic Sensor HC-SR04 and Arduino to distance calculation using Processing App**. Disponível em: https://www.javatpoint.com/iot-project-using-ultrasonic-sensor-arduino-distance-calculation. Acesso em: 18 out. 2024.

MAKER HERO. **Monitore o volume na sua caixa d'água**. Disponível em: https://www.makerhero.com/blog/monitore-o-volume-na-sua-caixa-dagua/. Acesso em: 23 out. 2024.

TINKERCAD. **Tinkercad: Create 3D digital designs with online CAD**. Disponível em: https://www.tinkercad.com/. Acesso em: 23 out. 2024.


