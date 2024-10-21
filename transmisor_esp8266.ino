#include <ESP8266WiFi.h>
#include <espnow.h>
#define ledverde 5

typedef struct {
    int id;
    char action;
} Message;

Message msg;

void setup() {
    pinMode(ledverde,OUTPUT);  
    Serial.begin(115200);
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();

    if (esp_now_init() != 0) {
        Serial.println("Error initializing ESP-NOW");
        return;
    }
    
    esp_now_set_self_role(ESP_NOW_ROLE_CONTROLLER);
    esp_now_register_send_cb(OnDataSent);

    msg.id = 8; // Cambia este número para cada carril
    msg.action = 'p';

    // Establecer dirección MAC de broadcast (envía a todos los dispositivos)
    uint8_t broadcastAddress[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};
    esp_now_add_peer(broadcastAddress, ESP_NOW_ROLE_SLAVE, 1, NULL, 0);
}

void loop() {
    if (digitalRead(14) == LOW) { // Cambia D1 al pin donde conectes el botón
        esp_now_send(NULL, (uint8_t *) &msg, sizeof(msg)); // Enviar por broadcast
        Serial.println("presionado");
        digitalWrite(ledverde,HIGH);
        delay(2000); // Para evitar múltiples envíos por un solo pulso
        digitalWrite(ledverde,LOW);
    }
}

void OnDataSent(uint8_t *mac_addr, uint8_t sendStatus) {
    Serial.print("Send Status: ");
    Serial.println(sendStatus == 0 ? "Success" : "Fail");
}


