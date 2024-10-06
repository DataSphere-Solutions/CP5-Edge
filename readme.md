# Edge Computing - CP5 - Data Logger / Dashboard
Olá, bem-vindo ao nosso trabalho do Check Point 5 de Edge Computing! Nós somos a empresa Data Sphere da turma 1ESPH, e é um imenso prazer apresentar este projeto.

![Data Sphere1000x1000](https://github.com/ianmonteirom/CP2-Edge/assets/152393807/0fe80a9b-6290-417d-8367-2abe3824d0b0)
Logo da nossa equipe
## O que é a Data Sphere?
A Data Sphere Solutions é uma empresa fictícia representando a nossa equipe, formada pelos alunos: 
-  <a href="https://www.linkedin.com/in/artur-alves-tenca-b1ba862b6/">Artur Alves</a> - RM 555171 
- <a href="https://www.linkedin.com/in/giuliana-lucas-85b4532b6/">Giuliana Lucas</a> - RM 557597
- <a href="https://www.linkedin.com/in/ian-monteiro-moreira-a4543a2b7/">Ian Monteiro</a> - RM 558652 
- <a href="https://www.linkedin.com/in/igor-brunelli-ralo-39143a2b7/">Igor Brunelli</a> - RM 555035
- <a href="https://www.linkedin.com/in/matheus-estev%C3%A3o-5248b9238/">Matheus Alcântara</a> - RM 558193

## Máquina Virtual hospedada na Nuvem
Utilizando a Microsoft Azure, hospedamos e configuramos uma máquina virtual (VM) com Ubuntu Server de sistema operacional. Nela, instalamos o Docker, o Docker Compose e o Fiware Descomplicado do professor Fábrio Cabrini, e abrimos as portas necessárias para todas as comunicações neste projeto serem possíveis.
![image](https://github.com/user-attachments/assets/40755ca2-5925-4e9e-a063-1c94e3953cbb)

## Simulação no Wokwi
Utilizando o simulador online Wokwi e configurando o código corretamente para a comunicação dos dados, podemos enviar os valores de luminosidade, umidade e temperatura captados pelos sensores LDR e DHT para o Postman:
![image](https://github.com/user-attachments/assets/6e7e57d1-fd03-48a4-8a38-1bcc5d2b7088)

- Link do Projeto: https://wokwi.com/projects/410952264842122241

## Postman
Utilizando o Postman para ler a coleção do API do Fiware Descomplicado (adaptado para este Checkpoint) e configurando o IP público da VM, fazemos os health checks e confirmamos que está tudo comunicando corretamente.
![image](https://github.com/user-attachments/assets/7b1031b4-1573-4ad7-8c35-3b113f16056a)
Através do Postman, podemos verificar os valores de luminosidade, umidade e temperatura que estão sendo enviados pelo Wokwi:
![image](https://github.com/user-attachments/assets/86e87e41-a210-4941-809e-d76d8e84cb9b)
![image](https://github.com/user-attachments/assets/f44b98dd-b6a7-4964-9c7f-73a24f7e3d8b)
![image](https://github.com/user-attachments/assets/56b9e19f-4f39-42fa-a841-9368b22966d7)

Podemos também pedir um número específico de valores históricos salvos pelo STH-Comet (neste caso, 30):
![image](https://github.com/user-attachments/assets/85022632-e4ed-4757-ab99-19e9d777d4f8)
![image](https://github.com/user-attachments/assets/5cf80513-415f-4bbc-94d9-60364efad37d)
![image](https://github.com/user-attachments/assets/6d64c188-ae32-4d70-b7ad-1f6a4d199741)

## Dashboard
Também desenvolvemos um Dashboard que recebe o JSON dos dados salvos e os plota em um gráfico, um para cada valor (luminosidade, umidade e temperatura), além de também plotar uma linha com o valor médio de cada um:
![image](https://github.com/user-attachments/assets/f76ef677-82e6-4090-aee8-48a0296e7496)
![image](https://github.com/user-attachments/assets/ac07984e-47bc-4899-9abc-c3a3a42446ed)


## Vídeo Explicativo no Youtube
- [Link do Vídeo](https://youtu.be/lVYydVUc0Go)




## Código do Projeto
```
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

// Configurações - variáveis editáveis
const char* default_SSID = "Wokwi-GUEST"; // Nome da rede Wi-Fi
const char* default_PASSWORD = ""; // Senha da rede Wi-Fi
const char* default_BROKER_MQTT = "20.197.230.60"; // IP do Broker MQTT
const int default_BROKER_PORT = 1883; // Porta do Broker MQTT
const char* default_TOPICO_SUBSCRIBE = "/TEF/sens002/cmd"; // Tópico MQTT de escuta
const char* default_TOPICO_PUBLISH_1 = "/TEF/sens002/attrs"; // Tópico MQTT de envio de informações para Broker
const char* default_TOPICO_PUBLISH_2 = "/TEF/sens002/attrs/l"; // Tópico MQTT de envio de informações para Broker
const char* default_TOPICO_PUBLISH_3 = "/TEF/sens002/attrs/t"; // Tópico MQTT para temperatura
const char* default_TOPICO_PUBLISH_4 = "/TEF/sens002/attrs/h"; // Tópico MQTT para umidade
const char* default_ID_MQTT = "fiware_002"; // ID MQTT

// Declaração da variável para o prefixo do tópico
const char* topicPrefix = "sens002";

// Variáveis para configurações editáveis
const char* SSID = default_SSID;
const char* PASSWORD = default_PASSWORD;
const char* BROKER_MQTT = default_BROKER_MQTT;
const int BROKER_PORT = default_BROKER_PORT;
const char* TOPICO_SUBSCRIBE = default_TOPICO_SUBSCRIBE;
const char* TOPICO_PUBLISH_1 = default_TOPICO_PUBLISH_1;
const char* TOPICO_PUBLISH_2 = default_TOPICO_PUBLISH_2;
const char* TOPICO_PUBLISH_3 = default_TOPICO_PUBLISH_3;
const char* TOPICO_PUBLISH_4 = default_TOPICO_PUBLISH_4;
const char* ID_MQTT = default_ID_MQTT;

// Definições do sensor DHT
#define DHTPIN 4          // Pino conectado ao DHT
#define DHTTYPE DHT22     // Tipo do sensor DHT (DHT11, DHT22, etc.)
DHT dht(DHTPIN, DHTTYPE);

// Definição do pino LDR
const int LDR_PIN = 34;

// Variáveis MQTT
WiFiClient espClient;
PubSubClient MQTT(espClient);

// Variáveis de temporização
unsigned long previousLuminosityMillis = 0;
unsigned long previousDHTMillis = 0;
const long intervalLuminosity = 1000; // 1 segundo
const long intervalDHT = 2000;         // 2 segundos

// Funções de inicialização
void initSerial() {
    Serial.begin(115200);
}

void initWiFi() {
    delay(10);
    Serial.println("------Conexao WI-FI------");
    Serial.print("Conectando-se na rede: ");
    Serial.println(SSID);
    Serial.println("Aguarde");
    reconectWiFi();
}

void initMQTT() {
    MQTT.setServer(BROKER_MQTT, BROKER_PORT);
    MQTT.setCallback(mqtt_callback);
}

void setup() {
    initSerial();
    initWiFi();
    initMQTT();
    dht.begin(); // Inicializa o sensor DHT
    delay(5000);
    // Publica estado inicial (opcional)
    MQTT.publish(TOPICO_PUBLISH_1, "Inicializado");
}

void loop() {
    VerificaConexoesWiFIEMQTT();
    
    unsigned long currentMillis = millis();
    
    // Handle Luminosity
    if (currentMillis - previousLuminosityMillis >= intervalLuminosity) {
        previousLuminosityMillis = currentMillis;
        handleLuminosity();
    }
    
    // Handle DHT Sensor
    if (currentMillis - previousDHTMillis >= intervalDHT) {
        previousDHTMillis = currentMillis;
        handleDHTSensor();
    }
    
    MQTT.loop();
}

// Funções de reconexão
void reconectWiFi() {
    if (WiFi.status() == WL_CONNECTED)
        return;
    WiFi.begin(SSID, PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
        delay(100);
        Serial.print(".");
    }
    Serial.println();
    Serial.println("Conectado com sucesso na rede ");
    Serial.print(SSID);
    Serial.println(" IP obtido: ");
    Serial.println(WiFi.localIP());
}

void reconnectMQTT() {
    while (!MQTT.connected()) {
        Serial.print("* Tentando se conectar ao Broker MQTT: ");
        Serial.println(BROKER_MQTT);
        if (MQTT.connect(ID_MQTT)) {
            Serial.println("Conectado com sucesso ao broker MQTT!");
            MQTT.subscribe(TOPICO_SUBSCRIBE);
        } else {
            Serial.println("Falha ao reconectar no broker.");
            Serial.println("Haverá nova tentativa de conexão em 2s");
            delay(2000);
        }
    }
}

// Callback MQTT
void mqtt_callback(char* topic, byte* payload, unsigned int length) {
    char message[length + 1];
    memcpy(message, payload, length);
    message[length] = '\0'; // Null-terminator
    String msg = String(message);
    
    Serial.print("- Mensagem recebida: ");
    Serial.println(msg);

    // Exemplo de processamento de comandos (a ajustar conforme necessidade)
    if (msg.equalsIgnoreCase("get_temp")) {
        float temperature = dht.readTemperature();
        if (!isnan(temperature)) {
            String tempStr = String(temperature, 2);
            MQTT.publish(TOPICO_PUBLISH_3, tempStr.c_str());
            Serial.println("- Temperatura enviada: " + tempStr);
        } else {
            Serial.println("- Falha na leitura da temperatura.");
        }
    }

    if (msg.equalsIgnoreCase("get_hum")) {
        float humidity = dht.readHumidity();
        if (!isnan(humidity)) {
            String humStr = String(humidity, 2);
            MQTT.publish(TOPICO_PUBLISH_4, humStr.c_str());
            Serial.println("- Umidade enviada: " + humStr);
        } else {
            Serial.println("- Falha na leitura da umidade.");
        }
    }
}

// Verifica conexões Wi-Fi e MQTT
void VerificaConexoesWiFIEMQTT() {
    if (!MQTT.connected()) {
        reconnectMQTT();
    }
    reconectWiFi();
}

// Envia dados de luminosidade
void handleLuminosity() {
    int sensorValue = analogRead(LDR_PIN);
    int luminosity = map(sensorValue, 0, 4095, 0, 100);
    String mensagem = String(luminosity);
    Serial.print("Valor da luminosidade: ");
    Serial.println(mensagem);
    MQTT.publish(TOPICO_PUBLISH_2, mensagem.c_str());
}

// Envia dados do sensor DHT
void handleDHTSensor() {
    float temperature = dht.readTemperature(); // Lê temperatura em Celsius
    float humidity = dht.readHumidity();       // Lê umidade relativa

    // Verifica se as leituras falharam
    if (isnan(temperature) || isnan(humidity)) {
        Serial.println("Falha ao ler do sensor DHT!");
        return;
    }

    // Publica temperatura
    String tempStr = String(temperature, 2);
    MQTT.publish(TOPICO_PUBLISH_3, tempStr.c_str());
    Serial.println("Valor da temperatura: " + tempStr);

    // Publica umidade
    String humStr = String(humidity, 2);
    MQTT.publish(TOPICO_PUBLISH_4, humStr.c_str());
    Serial.println("Valor da umidade: " + humStr);
}
```

## Código do Dashboard
```
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import requests
from datetime import datetime
import pytz

# Constants for IP and port
IP_ADDRESS = "20.197.230.60"
PORT_STH = 8666
DASH_HOST = "0.0.0.0"  # Set this to "0.0.0.0" to allow access from any IP

# Função para obter dados de luminosidade da API
def get_luminosity_data(lastN):
    url = f"http://{IP_ADDRESS}:{PORT_STH}/STH/v1/contextEntities/type/Sens/id/urn:ngsi-ld:Sens:002/attributes/luminosity?lastN={lastN}"
    headers = {
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        try:
            values = data['contextResponses'][0]['contextElement']['attributes'][0]['values']
            return values
        except KeyError as e:
            print(f"Key error (Luminosidade): {e}")
            return []
    else:
        print(f"Erro ao acessar {url}: {response.status_code}")
        return []

# Função para obter dados de temperatura da API
def get_temperature_data(lastN):
    url = f"http://{IP_ADDRESS}:{PORT_STH}/STH/v1/contextEntities/type/Sens/id/urn:ngsi-ld:Sens:002/attributes/temperature?lastN={lastN}"
    headers = {
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        try:
            values = data['contextResponses'][0]['contextElement']['attributes'][0]['values']
            return values
        except KeyError as e:
            print(f"Key error (Temperatura): {e}")
            return []
    else:
        print(f"Erro ao acessar {url}: {response.status_code}")
        return []

# Função para obter dados de umidade da API
def get_humidity_data(lastN):
    url = f"http://{IP_ADDRESS}:{PORT_STH}/STH/v1/contextEntities/type/Sens/id/urn:ngsi-ld:Sens:002/attributes/humidity?lastN={lastN}"
    headers = {
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        try:
            values = data['contextResponses'][0]['contextElement']['attributes'][0]['values']
            return values
        except KeyError as e:
            print(f"Key error (Umidade): {e}")
            return []
    else:
        print(f"Erro ao acessar {url}: {response.status_code}")
        return []

# Função para converter timestamps UTC para o fuso horário de São Paulo
def convert_to_sao_paulo_time(timestamps):
    utc = pytz.utc
    sao_paulo = pytz.timezone('America/Sao_Paulo')
    converted_timestamps = []
    for timestamp in timestamps:
        try:
            timestamp = timestamp.replace('T', ' ').replace('Z', '')
            converted_time = utc.localize(datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')).astimezone(sao_paulo)
        except ValueError:
            # Lidar com caso onde milissegundos não estão presentes
            converted_time = utc.localize(datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')).astimezone(sao_paulo)
        converted_timestamps.append(converted_time)
    return converted_timestamps

# Definir valor lastN
lastN = 10  # Obter os 10 pontos mais recentes a cada intervalo

# Inicializar a aplicação Dash
app = dash.Dash(__name__)

# Layout da Dashboard
app.layout = html.Div([
    html.H1('Data Sphere - Monitoramento dos valores do Sensor', style={'textAlign': 'center'}),
    
    # Gráfico de Luminosidade
    html.Div([
        html.H2('Luminosidade', style={'textAlign': 'center'}),
        dcc.Graph(id='luminosity-graph'),
        dcc.Store(id='luminosity-data-store', data={'timestamps': [], 'luminosity_values': []}),
    ], style={'padding': '20px'}),
    
    # Gráfico de Temperatura
    html.Div([
        html.H2('Temperatura', style={'textAlign': 'center'}),
        dcc.Graph(id='temperature-graph'),
        dcc.Store(id='temperature-data-store', data={'timestamps': [], 'temperature_values': []}),
    ], style={'padding': '20px'}),
    
    # Gráfico de Umidade
    html.Div([
        html.H2('Umidade', style={'textAlign': 'center'}),
        dcc.Graph(id='humidity-graph'),
        dcc.Store(id='humidity-data-store', data={'timestamps': [], 'humidity_values': []}),
    ], style={'padding': '20px'}),
    
    # Componente de Intervalo para atualização
    dcc.Interval(
        id='interval-component',
        interval=10*1000,  # em milissegundos (10 segundos)
        n_intervals=0
    )
])

# Callback para atualizar os dados de Luminosidade
@app.callback(
    Output('luminosity-data-store', 'data'),
    Input('interval-component', 'n_intervals'),
    State('luminosity-data-store', 'data')
)
def update_luminosity_data_store(n, stored_data):
    # Obter dados de luminosidade
    data_luminosity = get_luminosity_data(lastN)
    
    if data_luminosity:
        # Extrair valores e timestamps
        luminosity_values = [float(entry['attrValue']) for entry in data_luminosity]  # Garantir que os valores são floats
        timestamps = [entry['recvTime'] for entry in data_luminosity]
        
        # Converter timestamps para horário de São Paulo
        timestamps = convert_to_sao_paulo_time(timestamps)
        
        # Adicionar novos dados aos dados armazenados
        stored_data['timestamps'].extend(timestamps)
        stored_data['luminosity_values'].extend(luminosity_values)
        
        # Limitar o armazenamento a, por exemplo, 100 pontos para evitar sobrecarga
        if len(stored_data['timestamps']) > 100:
            stored_data['timestamps'] = stored_data['timestamps'][-100:]
            stored_data['luminosity_values'] = stored_data['luminosity_values'][-100:]
        
        return stored_data
    
    return stored_data

# Callback para atualizar os dados de Temperatura
@app.callback(
    Output('temperature-data-store', 'data'),
    Input('interval-component', 'n_intervals'),
    State('temperature-data-store', 'data')
)
def update_temperature_data_store(n, stored_data):
    # Obter dados de temperatura
    data_temperature = get_temperature_data(lastN)
    
    if data_temperature:
        # Extrair valores e timestamps
        temperature_values = [float(entry['attrValue']) for entry in data_temperature]
        timestamps = [entry['recvTime'] for entry in data_temperature]
        
        # Converter timestamps para horário de São Paulo
        timestamps = convert_to_sao_paulo_time(timestamps)
        
        # Adicionar novos dados aos dados armazenados
        stored_data['timestamps'].extend(timestamps)
        stored_data['temperature_values'].extend(temperature_values)
        
        # Limitar o armazenamento a 100 pontos
        if len(stored_data['timestamps']) > 100:
            stored_data['timestamps'] = stored_data['timestamps'][-100:]
            stored_data['temperature_values'] = stored_data['temperature_values'][-100:]
        
        return stored_data
    
    return stored_data

# Callback para atualizar os dados de Umidade
@app.callback(
    Output('humidity-data-store', 'data'),
    Input('interval-component', 'n_intervals'),
    State('humidity-data-store', 'data')
)
def update_humidity_data_store(n, stored_data):
    # Obter dados de umidade
    data_humidity = get_humidity_data(lastN)
    
    if data_humidity:
        # Extrair valores e timestamps
        humidity_values = [float(entry['attrValue']) for entry in data_humidity]
        timestamps = [entry['recvTime'] for entry in data_humidity]
        
        # Converter timestamps para horário de São Paulo
        timestamps = convert_to_sao_paulo_time(timestamps)
        
        # Adicionar novos dados aos dados armazenados
        stored_data['timestamps'].extend(timestamps)
        stored_data['humidity_values'].extend(humidity_values)
        
        # Limitar o armazenamento a 100 pontos
        if len(stored_data['timestamps']) > 100:
            stored_data['timestamps'] = stored_data['timestamps'][-100:]
            stored_data['humidity_values'] = stored_data['humidity_values'][-100:]
        
        return stored_data
    
    return stored_data

# Callback para atualizar o gráfico de Luminosidade
@app.callback(
    Output('luminosity-graph', 'figure'),
    Input('luminosity-data-store', 'data')
)
def update_luminosity_graph(stored_data):
    if stored_data['timestamps'] and stored_data['luminosity_values']:
        # Calcular a média da luminosidade
        mean_luminosity = sum(stored_data['luminosity_values']) / len(stored_data['luminosity_values'])
        
        # Criar as traces para o gráfico
        trace_luminosity = go.Scatter(
            x=stored_data['timestamps'],
            y=stored_data['luminosity_values'],
            mode='lines+markers',
            name='Luminosidade',
            line=dict(color='orange')
        )
        trace_mean = go.Scatter(
            x=[stored_data['timestamps'][0], stored_data['timestamps'][-1]],
            y=[mean_luminosity, mean_luminosity],
            mode='lines',
            name='Média Luminosidade',
            line=dict(color='blue', dash='dash')
        )
        
        # Criar a figura
        fig_luminosity = go.Figure(data=[trace_luminosity, trace_mean])
        
        # Atualizar o layout
        fig_luminosity.update_layout(
            title='Luminosidade ao Longo do Tempo',
            xaxis_title='Timestamp',
            yaxis_title='Luminosidade',
            hovermode='closest'
        )
        
        return fig_luminosity
    
    return {}

# Callback para atualizar o gráfico de Temperatura
@app.callback(
    Output('temperature-graph', 'figure'),
    Input('temperature-data-store', 'data')
)
def update_temperature_graph(stored_data):
    if stored_data['timestamps'] and stored_data['temperature_values']:
        # Calcular a média da temperatura
        mean_temperature = sum(stored_data['temperature_values']) / len(stored_data['temperature_values'])
        
        # Criar as traces para o gráfico
        trace_temperature = go.Scatter(
            x=stored_data['timestamps'],
            y=stored_data['temperature_values'],
            mode='lines+markers',
            name='Temperatura',
            line=dict(color='red')
        )
        trace_mean = go.Scatter(
            x=[stored_data['timestamps'][0], stored_data['timestamps'][-1]],
            y=[mean_temperature, mean_temperature],
            mode='lines',
            name='Média Temperatura',
            line=dict(color='green', dash='dash')
        )
        
        # Criar a figura
        fig_temperature = go.Figure(data=[trace_temperature, trace_mean])
        
        # Atualizar o layout
        fig_temperature.update_layout(
            title='Temperatura ao Longo do Tempo',
            xaxis_title='Timestamp',
            yaxis_title='Temperatura (°C)',
            hovermode='closest'
        )
        
        return fig_temperature
    
    return {}

# Callback para atualizar o gráfico de Umidade
@app.callback(
    Output('humidity-graph', 'figure'),
    Input('humidity-data-store', 'data')
)
def update_humidity_graph(stored_data):
    if stored_data['timestamps'] and stored_data['humidity_values']:
        # Calcular a média da umidade
        mean_humidity = sum(stored_data['humidity_values']) / len(stored_data['humidity_values'])
        
        # Criar as traces para o gráfico
        trace_humidity = go.Scatter(
            x=stored_data['timestamps'],
            y=stored_data['humidity_values'],
            mode='lines+markers',
            name='Umidade',
            line=dict(color='blue')
        )
        trace_mean = go.Scatter(
            x=[stored_data['timestamps'][0], stored_data['timestamps'][-1]],
            y=[mean_humidity, mean_humidity],
            mode='lines',
            name='Média Umidade',
            line=dict(color='purple', dash='dash')
        )
        
        # Criar a figura
        fig_humidity = go.Figure(data=[trace_humidity, trace_mean])
        
        # Atualizar o layout
        fig_humidity.update_layout(
            title='Umidade ao Longo do Tempo',
            xaxis_title='Timestamp',
            yaxis_title='Umidade (%)',
            hovermode='closest'
        )
        
        return fig_humidity
    
    return {}

# Executar o servidor Dash
if __name__ == '__main__':
    app.run_server(debug=True, host=DASH_HOST, port=8050)
```
