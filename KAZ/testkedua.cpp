#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <MPU6050_light.h>


// Update these with values suitable for your network.

const char* ssid = "abcd";
const char* password = "12345678";
const char* mqtt_server = "0.tcp.ap.ngrok.io";  // test.mosquitto.org

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE	(50)
char msg[MSG_BUFFER_SIZE];
int value = 0;
MPU6050 mpu(Wire);
int timer = 0;

void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Switch on the LED if an 1 was received as first character
  if ((char)payload[0] == '1') {
    digitalWrite(BUILTIN_LED, LOW);   // Turn the LED on (Note that LOW is the voltage level
    // but actually the LED is on; this is because
    // it is active low on the ESP-01)
  } else {
    digitalWrite(BUILTIN_LED, HIGH);  // Turn the LED off by making the voltage HIGH
  }

}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("device/temp", "MQTT Server is Connected");
      // ... and resubscribe
      client.subscribe("device/led");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);      
  setup_wifi();
  client.setServer(mqtt_server, 19636);                                        
  Wire.begin();
  mpu.begin();
  Serial.println(F("Calculating gyro offset, do not move MPU6050"));       
  mpu.calcGyroOffsets();
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  mpu.update();  
  if((millis()-timer)>500)                         // print data every 500ms
  {                                                                   
    Serial.print("P : ");
    Serial.print(mpu.getAngleX());
    value=mpu.getAngleX();
    snprintf (msg, MSG_BUFFER_SIZE, "X :%ld", mpu.getAngleX());
    client.publish("Arduino/Gyro", msg);
    Serial.print(" | R : ");
    Serial.print(mpu.getAngleY());
    Serial.print(" | Y : ");
    Serial.println(mpu.getAngleZ());                
    timer = millis();  
  }
}