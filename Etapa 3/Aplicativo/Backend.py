# Entradas do usuário no aplicativo
consumo_m3 = 200
custo_total = 4000

# consumo_m3 = float(input("\n\nInforme o consumo registrado pelo hidrômetro no mês (em m³): "))
# custo_total = float(input("\nInforme o custo total da água no mês (em R$): "))

# Função para calcular o custo por litro de água
def calcular_custo_por_litro(consumo_m3, custo_total):
    consumo_litros = consumo_m3 * 1000  # Converte para litros
    custo_por_litro = custo_total / consumo_litros
    return custo_por_litro

# Variável responsável pelo custo por litro
custo_litro = calcular_custo_por_litro(consumo_m3, custo_total)

# Exibindo os resultados
print(f"\n\nCusto por litro de água: R$ {custo_litro:.2f} por litro")

# Variáveis vindas do microocontolador 
Q = [8, 1, 19, 8, 19, 16, 23, 24, 15, 24, 13, 1, 7, 8, 21, 23, 8, 13, 3, 5, 17, 25, 5, 4] # Em litros
volume_caixa = 500

# Função responsável pelo consumo na última hora
def consumo_hora(Q, custo_litro):
    return Q * custo_litro

consumo_ultima_hora = consumo_hora(Q[0], custo_litro)

print(f"\nCusto na útima hora: R$ {consumo_ultima_hora:.2f}")
print(f"Volume de água gasto na última hora: {Q[0]:.2f} litros")

# Função resposável pelo consumo no dia
Consumo_dia = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # Em litros

for i in range(24):  
    Consumo_dia[0] += Q[i] 

def consumo_no_dia(Consumo_dia, custo_litro):
    return Consumo_dia * custo_litro

Custo_dia = consumo_no_dia(Consumo_dia[0], custo_litro)

print(f"\nCurso da água no dia: R$ {Custo_dia:.2f}")

print(f"Volume de agua gasto no dia: R$ {Consumo_dia[0]:.2f} Litros")

# Função responsável pelo consumo no mês

Consumo_mes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # Em litros

for i in range(30):  
    Consumo_mes[0] += Consumo_dia[i]

def consumo_no_mes(Consumo_mes, custo_litro):
    return Consumo_mes * custo_litro

Custo_mes = consumo_no_mes(Consumo_mes[0], custo_litro)

print(f"\nCurso da água no mês: R$ {Custo_mes:.2f}")

print(f"Volume de agua gasto no dia: R$ {Consumo_mes[0]:.2f} Litros")

# Função responsável pelo consumo no ano

Consumo_ano = [0, 0, 0, 0, 0] # Em litros

for i in range(5):  
    Consumo_ano[0] += Consumo_mes[i]

def consumo_no_ano(Consumo_ano, custo_litro):
    return Consumo_ano * custo_litro

Custo_ano = consumo_no_ano(Consumo_ano[0], custo_litro)

print(f"\nCurso da água no ano: R$ {Custo_ano:.2f}")

print(f"Volume de agua gasto no ano: R$ {Consumo_ano[0]:.2f} Litros")

# Água disponível na caixa d'água

Agua_disponivel = volume_caixa

print(f"\nVolume de água disponível na caixa água: {Agua_disponivel:.0f} litros")

# Consumo real (diferença em reais com o valor do hidrômetro)

# Inserido pelo usuário no aplicativo
Consumo_Hidrometro = float(input("\nInforme o custo total da água neste mês (em R$): "))

Difereca = Consumo_Hidrometro - Custo_mes

if Difereca < 0:
    print(f"\nO cusumo do seu hidrometro está de acordo com o seu consumo da caixa :)")
else:
    def Difereca_consumo(Difereca, Consumo_Hidrometro):
        Dif = Difereca * 100
        porcentagem_dif = Dif / Consumo_Hidrometro
        return porcentagem_dif
    
    P_consumo_real = Difereca_consumo(Difereca, Consumo_Hidrometro)

    print(f"\nA difereça entre o consumo do hidrômetro e do equipamento é de {P_consumo_real:.2f}%")

    print(f"O que caracteriza uma difereça de R$ {Difereca:.2f} ")
