# Codigo de Desenvolvimento - Falta os testes.
# Status: Validar o funcionamento
# Este código recebe as messagens do broker e guarda num ficheiro JSON
# Import dos modulos de mqtt para tratar as mensagens
import paho.mqtt.client as mqtt
import json

# Cria uma lista na variavel messages.
#messages = []
alarmes = {}
messages = {}
# Função que recebe os topicos do broker
def on_message(client, userdata, msg):
    # carrega a mensagem na variavel
    message_data = {
        "topic": msg.topic,
        "payload": json.loads(msg.payload.decode("utf-8"))
    }
    
    
    # Faz o dump das mensagens recebidas para o ficheiro JSON
    if msg.topic not in messages:
        messages[msg.topic] = []  # Initialize a list for new topics
    messages[msg.topic].append(message_data) 
    #messages.append(message_data)
    with open("received_messages.json", "w") as file:
        json.dump(messages, file, indent=4)

    if msg.topic not in alarmes:
        alarmes[msg.topic] = []  # Incializa a lista para novos topicos


    # Alarme do device Frigorifico, valida a temperatura para
    # ser o ideal na conservação de alimentos
    # Temperatura acima de 3 e inferiror a 4, Temperatura Alta
    # Temperatura acima ou igual a 5, Temperatura critica 
    if "frigorifico" in msg.topic:
        # Definição das variaveis com dados do sensor
        temperatura = message_data['payload']['temperatura']
        timestamp = message_data['payload']['timestamp']
        porta_aberta = message_data["payload"]["porta_aberta"]
        device = message_data['payload']['Device']
        # Condicões para acionar os alarmes
        if temperatura > 3 and temperatura <= 3.9:
            alarmes[msg.topic].append({"Criticidade":"ALTO","device":device,"Timestamp":timestamp,"Temperatura":temperatura})
            # Print do Alarme
            print(f"ALARME ALTO: - Temperatura do {device} é {temperatura}ºC, está elevada! acima dos 3ºC!")
        elif temperatura >=5:
            alarmes[msg.topic].append({"Criticidade":"CRITICO","Device":device,"Timestamp":timestamp,"Temperatura":temperatura})
            # Print do Alarme
            print(f"ALARME CRITICO: - Temperatura do {device} é {temperatura}ºC, intervenção urgente! acima dos 5ºC!")
        
        # Alarme Porta aberta
        if porta_aberta == True:
            alarmes[msg.topic].append({"Criticidade": "ALERTA", "device":device,"Timestamp":timestamp,"Porta_Aberta":porta_aberta})
            # Print alarme
            print(f"ALERTA: - A porta do {device} ficou aberta, fechar a porta!")
        
    
        # Alarme da casa valida a temperatura para regulação do
        # ar condicionado e se a luz da casa fif "casa" in msg.topic:
        # Definição das variaveis com da    dos do sensor
    if "casa" in msg.topic:
        temp_casa = message_data['payload']['temperatura']
        timestamp = message_data['payload']['timestamp']
        luz_acesa = message_data['payload']['Luz acesa']
        device = message_data['payload']['Device']
        # Condicões para acionar os alarmes
        # valida intervalos de temperatura
        if temp_casa <23:
            alarmes[msg.topic].append({"Criticidade":"FRIO","device":device,"Timestamp":timestamp,"Temperatura":temp_casa})
            # Print do Alarme
            print(f"Frio {temp_casa}ºC ajustar ar condicionado da {device} para mais calor!")
        elif temp_casa > 25 and temp_casa >=41:
            alarmes[msg.topic].append({"Criticidade":"CALOR","device":device,"Timestamp":timestamp,"Temperatura":temp_casa})
            # Para validar o funcionamento
            print(f"Calor {temp_casa} ajustar ar condicionado para mais frio!")
        elif temp_casa >=41:
            alarmes[msg.topic].append({"Criticidade":"CALOR ELEVADO","Device":device,"Timestamp":timestamp,"Temperatura":temp_casa})
            # Print do Alarme
            print(f"Muito Calor! {temp_casa}ºC ajustar o ar condicionado da {device} para mais frio urgente!")
        
        # valida se a luz ficou acesa
        if luz_acesa == True:
            alarmes[msg.topic].append({"Criticidade":"ALERTA","Device":device,"Timestamp":timestamp,"Luz acesa":luz_acesa})
            # Print do Alarme
            print(f"A luz da {device} ficou acesa!!!")


    # Alarme do device jardim valida a humidade da terra,
    # para controlar a rega.            
    if "jardim" in msg.topic:
        humidade = message_data['payload']['Humidade Terra']
        timestamp = message_data['payload']['timestamp']
        device = message_data['payload']['Device']
        if humidade <= 40:
            alarmes[msg.topic].append({"Criticidade":"ALTA","Device":device,"Timestamp":timestamp,"Humidade Terra":humidade})
            # Print do Alarme
            print(f"Humidade do {device} a {humidade}% abaixo dos 40%, fazer moderada urgente!")
        elif humidade <= 60:
            alarmes[msg.topic].append({"Criticidade":"ALERTA","Device":device,"Timestamp":timestamp,"Humidade Terra":humidade})
            # Print do Alarme
            print(f"Humidade do {device} a {humidade}% abaixo dos 60%, fazer rega moderada!")


    # Grava a lista de alarmes para um ficheiro JSON
    with open("alarmes.json","w") as file:
        json.dump(alarmes, file, indent=4)
    
    #print(alarmes)


#Ligação ao broker  
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
#Chama a função on_message
client.on_message = on_message
#Configuração de acesso ao broker, colocar o endreço de IP do broker
client.connect("192.168.68.123", 1883)
#Filtro do topico a receber, está com Wildcard
client.subscribe("#")
#Fica em loop á escuta
client.loop_forever()

