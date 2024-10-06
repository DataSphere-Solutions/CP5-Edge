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
