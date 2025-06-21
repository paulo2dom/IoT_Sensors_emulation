#Sensor de frigorifico
#Este emulador gera valores de um sensor de Frigorifico, com a temperatura,
#sem tem a porta aberta e consumo de energia

#### Ver com os apontamentos dos Slides a Classes ######

#importa modulos
import time
import json
import random as ra
from datetime import datetime
import paho.mqtt.client as mqtt

# Class base para os sensores
class Sensor:
    def simula(self):
        raise NotImplementedError("Subclasses devem implementar este método")

# Frigorifico class sensor
class FrigorificoSensor(Sensor):
    '''Simula sensores de Frigorifico'''
    def simula(self):
        # Dicionário para gerar valores e retorna um dump de JSON
        return json.dumps({
                "Device":"Frigorifico",
                #Valores dos sensores do frigorifico
                "timestamp": datetime.now().astimezone().isoformat(),
                "temperatura": round(ra.uniform(0, 8), 2),
                "porta_aberta": ra.choice([True, False]),
                "consumo_energia": round(ra.uniform(200, 350), 2)
        })

# Casa class sensor
class CasaSensor(Sensor):
    def simula(self):
        # Dicionário para gerar valores e retorna um dump de JSON
        return json.dumps({
                "Device":"Casa",
                # Valores dos sensores da casa
                "timestamp": datetime.now().astimezone().isoformat(),
                "temperatura": round(ra.uniform(0, 50), 2),
                "Humidade": round(ra.uniform(15, 100), 2),
                "Luz acesa": ra.choice([True, False])
        })

# Jardim class sensor
class JardimSensor(Sensor):
    def simula(self):
        # Dicionário para gerar valores e retorna um dump de JSON
        return json.dumps({
                "Device":"Jardim_Rega",
                #Valores dos sensores do Jardim
                "timestamp": datetime.now().astimezone().isoformat(),
                "Humidade Terra": round(ra.uniform(30, 100), 2)
        })

# Configuração do cliente MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("192.168.68.123", 1883, 60)

# Cria instancias Sensores
frigorifico_sensor = FrigorificoSensor()
casa_sensor = CasaSensor()
jardim_sensor = JardimSensor()

# Inicio loop
while True:
    #Declara as variaveis com os dados definidos nas classes
    data_frigorifico = frigorifico_sensor.simula()
    data_casa = casa_sensor.simula()
    data_jardim = jardim_sensor.simula()
    
    #Publica a informação no Broker
    client.publish("iot/sensores/frigorifico", data_frigorifico)
    client.publish("iot/sensores/casa", data_casa)
    client.publish("iot/sensores/jardim", data_jardim)
    
    #Faz print da informação enviada e espera 5 segundos em cada ação
    print(f"Dados enviados: {data_frigorifico}")
    time.sleep(1)
    print(f"Dados enviados: {data_casa}")
    time.sleep(1)
    print(f"Dados enviados: {data_jardim}")
    time.sleep(1)