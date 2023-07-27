#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <MPU6050_light.h>
#include <Adafruit_MPU6050.h>
#include <SPI.h>
#include <SD.h>

const int chipSelect = D8;

Adafruit_MPU6050 adampu;
int16_t ax, ay, az;
int16_t gx, gy, gz;
sensors_event_t a, g, temp;

//Gyroscope sensor deviation
float gyroXerror = 0.07;
float gyroYerror = 0.03;
float gyroZerror = 0.01;

float gyroX, gyroY, gyroZ;
float accX, accY, accZ;
float degX, degY, degZ;

struct MyData {
  byte X;
  byte Y;
  byte Z;
};

MyData data;

// Update these with values suitable for your network.
const char *ssid = "Kazarach IP";
const char *password = "modalcok";
const char *mqtt_server = "0.tcp.ap.ngrok.io";  // test.mosquitto.org

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE (50)
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

void callback(char *topic, byte *payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Switch on the LED if an 1 was received as first character
  if ((char)payload[0] == '1') {
    digitalWrite(BUILTIN_LED, LOW);  // Turn the LED on (Note that LOW is the voltage level
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

void gyroScope() {
  adampu.getEvent(&a, &g, &temp);

  float gyroX_temp = g.gyro.x;
  if (abs(gyroX_temp) > gyroXerror) {
    gyroX += gyroX_temp / 50.00;
  }

  float gyroY_temp = g.gyro.y;
  if (abs(gyroY_temp) > gyroYerror) {
    gyroY += gyroY_temp / 70.00;
  }

  float gyroZ_temp = g.gyro.z;
  if (abs(gyroZ_temp) > gyroZerror) {
    gyroZ += gyroZ_temp / 90.00;
  }
  Serial.println("GYROSCOPE");
  Serial.print("X = ");
  Serial.print(gyroX);
  Serial.print(" rad/s  |");
  snprintf(msg, MSG_BUFFER_SIZE, "1 %.2f", gyroX);
  client.publish("Arduino/GYRO X |", msg);
  Serial.print("Y = ");
  Serial.print(gyroY);
  Serial.print(" rad/s  |");
  snprintf(msg, MSG_BUFFER_SIZE, "2 %.2f", gyroY);
  client.publish("Arduino/GYRO Y |", msg);
  Serial.print("Z = ");
  Serial.print(gyroZ);
  Serial.println(" rad/s");
  snprintf(msg, MSG_BUFFER_SIZE, "3 %.2f", gyroZ);
  client.publish("Arduino/GYRO Z |", msg);
}

void accelerometer() {
  adampu.getEvent(&a, &g, &temp);
  // Get current acceleration values
  accX = a.acceleration.x;
  accY = a.acceleration.y;
  accZ = a.acceleration.z;
  Serial.println("ACCELEROMETER");
  Serial.print("X = ");
  Serial.print(accX);
  Serial.print(" m/s2  |");
  snprintf(msg, MSG_BUFFER_SIZE, "4 %.2f", accX);
  client.publish("Arduino/ACC X |", msg);
  Serial.print("Y = ");
  Serial.print(accY);
  Serial.print(" m/s2  |");
  snprintf(msg, MSG_BUFFER_SIZE, "5 %.2f", accY);
  client.publish("Arduino/ACC Y |", msg);
  Serial.print("Z = ");
  Serial.print(accZ);
  Serial.println(" m/s2");
  snprintf(msg, MSG_BUFFER_SIZE, "6 %.2f", accZ);
  client.publish("Arduino/ACC Z |", msg);
}

void degree() {
  mpu.update();

  Serial.print("P : ");
  degX = mpu.getAngleX();
  Serial.print(degX);
  snprintf(msg, MSG_BUFFER_SIZE, "7 %.2f", degX);
  client.publish("Arduino/6 Degree Freedom X |", msg);
  Serial.print(" | R : ");
  degY = mpu.getAngleY();
  Serial.print(degY);
  snprintf(msg, MSG_BUFFER_SIZE, "8 %.2f", degY);
  client.publish("Arduino/6 Degree Freedom Y |", msg);
  Serial.print(" | Y : ");
  degZ = mpu.getAngleZ();
  Serial.println(degZ);
  snprintf(msg, MSG_BUFFER_SIZE, "9 %.2f", degZ);
  client.publish("Arduino/6 Degree Freedom Z |", msg);
}

void saving_data() {
  File dataFile = SD.open("data.txt", FILE_WRITE);
  if (dataFile) {
    dataFile.printf("%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n", gyroX, gyroY, gyroZ, accX, accY, accZ, degX, degY, degZ);
    dataFile.close();
    Serial.println("Berhasil menulis data ke berkas data.txt.");
  } else {
    Serial.println("Gagal membuat atau membuka berkas data.txt.");
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 13533);
  if (!SD.begin(chipSelect)) {
    Serial.println("Kartu microSD tidak terdeteksi!");
    return;
  }
  Serial.println("Kartu microSD terdeteksi!");
  SD.remove("data.txt");
  Wire.begin();
  adampu.begin();
  Serial.println(F("Calculating gyro offset, do not move MPU6050"));
  mpu.calcGyroOffsets();
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  gyroScope();
  accelerometer();
  degree();
  saving_data();
  delay(1000);
}
