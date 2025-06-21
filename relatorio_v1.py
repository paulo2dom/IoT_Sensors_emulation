#Carrega o modulo de JSON
import json

# Caminho onde se encontra o ficheiro JSON
relatorio_path = "received_messages.json"
relatorio_alarmes_path = "alarmes.json"

#Função para ler o ficheiro para os relatórios JSON
def relatorio(relatorio_path):
    with open(relatorio_path, "r") as f:
        relatorio_data = json.load(f)    
    return relatorio_data

#Função para ler o ficheiro para os relatórios de Alarmes JSON
def relatorio(relatorio_alarmes_path):
    with open(relatorio_alarmes_path, "r") as f:
        relatorio_alarmes = json.load(f)    
    return relatorio_alarmes


# Inicio Relatório Frigorifico
# insere na Variavel a lista mensagens dos sensores do Frigorifico
relatorio_calcs = relatorio(relatorio_path)["iot/sensores/frigorifico"]
#Insere na variavel a lista de mensagens de alarme do Frigorifico
Alarmes_relatorio = relatorio(relatorio_alarmes_path)["iot/sensores/frigorifico"]
#Insere na variavel o relatório na variavel estatisticas da Casa 
relatorio_calcs_casa = relatorio(relatorio_path)["iot/sensores/casa"]
#Insere na variavel as mensagens de alarme da Casa
Alarmes_relatorio_casa = relatorio(relatorio_alarmes_path)["iot/sensores/casa"]
#Insere na variavel o relatório na variavel estatisticas da Casa 
relatorio_calcs_jardim = relatorio(relatorio_path)["iot/sensores/jardim"]
#Insere na variavel as mensagens de alarme da Casa
Alarmes_relatorio_jardim = relatorio(relatorio_alarmes_path)["iot/sensores/jardim"]



################################################
######## Relatório do Frigorifico  ############
###############################################

#Inicializa as variaveis 
Total_temperatura = 0
Total_consumo = 0
Count_consumo = 0
count = 0
#For para fazer o count de amostras e a soma destas.
for item in relatorio_calcs:
    temperatura = item['payload']['temperatura']
    Consumo = item['payload']['consumo_energia']
    Total_temperatura += temperatura
    count +=1
    Total_consumo += Consumo
    Count_consumo += 1



# Calcula a média 
average_temperatura = round(Total_temperatura / count, 2)    
average_consumo = round(Total_consumo / Count_consumo, 2)
#Imprime relatório Frigorifico
sensor = item['payload']['Device']
print("============== RELATÒRIO DO DEVICE FRIGORIFICO ================")
print(f"\nA média da temperatura do {sensor} é:{average_temperatura}ºC")
print(f"Consumo total é de {round(Total_consumo,2)}Kwh e a média do consumo é {average_consumo}Kwh")

#Inicializa as variaveis 
Total_temp_alarme = 0
count_alarme_critico = 0
count_alarme_alto = 0
count_porta_aberta = 0

#For para fazer o count de amoAlarmes_relatoriostras e a soma destas.
for item in Alarmes_relatorio:
    if item['Criticidade'] == "CRITICO":
        Total_temp_alarme += item['Temperatura']
        count_alarme_critico +=1
    elif item['Criticidade'] == "ALTO":
        Total_temp_alarme += item['Temperatura']
        count_alarme_alto +=1
    if item['Criticidade'] == "ALERTA":
        count_porta_aberta += item['Porta_Aberta']

# Cria listas para armazenar alarms
critico_alarms = []
alto_alarms = []
porta_aberta = []

for item in Alarmes_relatorio:
    if item['Criticidade'] == "CRITICO":
        critico_alarms.append((item['Timestamp'], item['Temperatura']))
    elif item['Criticidade'] == "ALTO":
        alto_alarms.append((item['Timestamp'], item['Temperatura']))
    elif item['Criticidade'] == "ALERTA":
        porta_aberta.append((item['Timestamp'], item['Porta_Aberta']))

# Sort the lists by timestamp
critico_alarms.sort()
alto_alarms.sort()
porta_aberta.sort()

#Print de alarmes Criticos
print("\nALARMES CRITICOS:")
print(f"O numero Total de alarmes Criticos foram:{count_alarme_critico}")
# Print da lista ordenada dos alarmes criticos
for timestamp, temperatura in critico_alarms:
    print(f"Timestamp: {timestamp}, Temperatura: {temperatura}")

#Printe de alarmes Altos
print("\nALARMES ALTOS:")
print(f"O numero Total de alarmes Altos foram:{count_alarme_alto}")
# Print da lista ordenada dos alarmes Altos
for timestamp, temperatura in alto_alarms:
    print(f"Timestamp: {timestamp}, Temperatura: {temperatura}")

print("\nPORTA ABERTA:")
print(f"O numero de vezes porta aberta :{count_porta_aberta}")
# Print da lista ordenada dos Altos
for timestamp, porta_aberta in porta_aberta:
    if porta_aberta == True:
        porta = "Aberta"
    print(f"Timestamp: {timestamp}, Porta: {porta}")



########################################################################

################################################
############ Relatório da Casa  ###############
##############################################

#Inicializa as variaveis 
Total_temp_casa = 0
Total_humidade_casa = 0
count_temp_casa = 0
count_humid_casa = 0

#For para fazer o count de amostras e a soma destas.
for item in relatorio_calcs_casa:
    temp_casa = item['payload']['temperatura']
    Humd_casa = item['payload']['Humidade']
    Total_temp_casa += temp_casa
    count_temp_casa +=1
    Total_humidade_casa += Humd_casa
    count_humid_casa +=1
# Calcula a média 
average_temp_casa = round(Total_temp_casa / count_temp_casa, 2)
average_Humidade_casa = round(Total_humidade_casa / count_humid_casa, 2)
#Imprime relatório Frigorifico
sensor = item['payload']['Device']

print("\n============== RELATÒRIO DO DEVICE CASA ================")
print(f"\nA média da temperatura da {sensor} é:{average_temp_casa}ºC")
print(f"A média da húmidade da {sensor} é:{average_Humidade_casa}%")

#Inicializa as variaveis 
Total_temp_alarme_casa = 0
count_alarme_frio_casa = 0
count_alarme_alerta_casa = 0
count_alarme_calor_casa = 0


#For para fazer o count de amoAlarmes_relatoriostras e a soma destas.
for item in Alarmes_relatorio_casa:
    if item['Criticidade'] == "FRIO":
        Total_temp_alarme_casa += item['Temperatura']
        count_alarme_frio_casa +=1
    elif item['Criticidade'] == "CALOR":
        Total_temp_alarme_casa += item['Temperatura']
        count_alarme_calor_casa +=1
    if item['Criticidade'] == "ALERTA":
       count_alarme_alerta_casa += item['Luz acesa']
        
# Cria listas para armazenar alarms
alarms_frio_casa = []
alarms_calor_casa = []
alarms_luz_acesa_casa = []

for item in Alarmes_relatorio_casa:
    if item['Criticidade'] == "FRIO":
        alarms_frio_casa.append((item['Timestamp'], item['Temperatura']))
    elif item['Criticidade'] == "CALOR":
        alarms_calor_casa.append((item['Timestamp'], item['Temperatura']))
    elif item['Criticidade'] == "ALERTA":
        alarms_luz_acesa_casa.append((item['Timestamp'], item['Luz acesa']))

# Sort the lists by timestamp
alarms_frio_casa.sort()
alarms_calor_casa.sort()
alarms_luz_acesa_casa.sort()

#Print de alarmes Criticos
print("\nALARMES DE FRIO:")
print(f"O numero Total de alarmes de frio foram:{count_alarme_frio_casa}")
# Print da lista ordenada dos alarmes criticos
for timestamp, temperatura in alarms_frio_casa:
    print(f"Timestamp: {timestamp}, Temperatura: {temperatura}")

#Printe de alarmes Altos
print("\nALARMES DE CALOR:")
print(f"O numero Total de alarmes de calor foram:{count_alarme_calor_casa}")
# Print da lista ordenada dos alarmes Altos
for timestamp, temperatura in alarms_calor_casa:
    print(f"Timestamp: {timestamp}, Temperatura: {temperatura}")

print("\nALERTA LUZ ACESA:")
print(f"O numero de vezes que a luz ficou acesa :{count_alarme_alerta_casa}")
# Print da lista ordenada dos alertas
for timestamp, alarms_luz_acesa_casa  in alarms_luz_acesa_casa:
   if alarms_luz_acesa_casa == True:
        Luz = "Acesa"
        print(f"Timestamp: {timestamp}, A Luz ficou: {Luz}")

################################################
############ Relatório do Jardim ##############
##############################################

#Inicializa as variaveis 
Total_humid_jardim = 0
count_humid_jardim = 0

#For para fazer o count de amostras e a soma destas.
for item in relatorio_calcs_jardim:
    Humid_jardim = item['payload']['Humidade Terra']
    Total_humid_jardim += Humid_jardim
    count_humid_jardim +=1

# Calcula a média 
average_humid_jardim = round(Total_humid_jardim / count_humid_jardim, 2)

#Imprime relatório Frigorifico
sensor = item['payload']['Device']

print("\n============== RELATÒRIO DO DEVICE JARDIM ================")
print(f"\nA média da humidade do {sensor} é:{average_humid_jardim}ºC")

#Inicializa as variaveis 
Total_humid_jardim = 0
count_alarme_alerta_jardim = 0
count_alarme_alta_jardim = 0

#For para fazer o count de amoAlarmes_relatoriostras e a soma destas.
for item in Alarmes_relatorio_jardim:
    if item['Criticidade'] == "ALERTA":
        Total_humid_jardim += item['Humidade Terra']
        count_alarme_alerta_jardim +=1
    elif item['Criticidade'] == "ALTA":
        Total_humid_jardim += item['Humidade Terra']
        count_alarme_alta_jardim +=1
        
# Cria listas para armazenar alarms
alarms_alerta_jardim = []
alarms_alta_jardim = []

for item in Alarmes_relatorio_jardim:
    if item['Criticidade'] == "ALERTA":
        alarms_alerta_jardim.append((item['Timestamp'], item['Humidade Terra']))
    elif item['Criticidade'] == "ALTA":
        alarms_alta_jardim.append((item['Timestamp'], item['Humidade Terra']))
    
# Sort the lists by timestamp
alarms_alerta_jardim.sort()
alarms_alta_jardim.sort()

#Print de alarmes Criticos
print("\nALARMES DE ALERTA:")
print(f"O numero Total de alertas foram:{count_alarme_alerta_jardim}")
# Print da lista ordenada dos alarmes criticos
for timestamp, alarms_alerta_jardim in alarms_alerta_jardim:
    print(f"Timestamp: {timestamp}, Temperatura: {alarms_alerta_jardim}")

#Printe de alarmes criticidade Alta
print("\nALARMES CRITICIDADE ALTA:")
print(f"O numero Total de alarmes criticidade alta foram:{count_alarme_alta_jardim}")
# Print da lista ordenada dos alarmes Altos
for timestamp, alarms_alta_jardim in alarms_alta_jardim:
    print(f"Timestamp: {timestamp}, Temperatura: {alarms_alta_jardim}")
    