#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <MPU6050.h>
#include <Adafruit_MPU6050.h>
#include <SPI.h>
#include <SD.h>

const unsigned long interval1 = 1000;  
const unsigned long interval2 = 100;   
const unsigned long interval3 = 5000;

unsigned long previousMillis1 = 0;  // Menyimpan waktu terakhir delay 1
unsigned long previousMillis2 = 0;  // Menyimpan waktu terakhir delay 2
unsigned long previousMillis3 = 0;  // Menyimpan waktu terakhir delay 3

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

MPU6050 mpu;

// Konstanta Kalman Filter
const float Q_angle = 0.001;   // Variance dari estimasi ketidakpastian sensor
const float Q_bias = 0.003;    // Variance dari estimasi ketidakpastian bias
const float R_measure = 0.03;  // Variance dari ketidakpastian pengukuran

// State Kalman Filter untuk setiap sumbu
float angle_pitch = 0;  // Sudut hasil estimasi Pitch
float angle_roll = 0;   // Sudut hasil estimasi Roll
float angle_yaw = 0;    // Sudut hasil estimasi Yaw

float bias_pitch = 0;  // Bias hasil estimasi Pitch
float bias_roll = 0;   // Bias hasil estimasi Roll
float bias_yaw = 0;    // Bias hasil estimasi Yaw

float rate_pitch = 0;  // Derivatif sudut dari sensor Pitch
float rate_roll = 0;   // Derivatif sudut dari sensor Roll
float rate_yaw = 0;    // Derivatif sudut dari sensor Yaw

// Posisi Covariance untuk setiap sumbu
float P_pitch[2][2] = { { 0, 0 }, { 0, 0 } };
float P_roll[2][2] = { { 0, 0 }, { 0, 0 } };
float P_yaw[2][2] = { { 0, 0 }, { 0, 0 } };

float gyroX_5s[5]={0,0,0,0,0};
float gyroY_5s[5]={0,0,0,0,0};
float gyroZ_5s[5]={0,0,0,0,0};

float accX_5s[5]={0,0,0,0,0};
float accY_5s[5]={0,0,0,0,0};
float accZ_5s[5]={0,0,0,0,0};

float pitch_5s[5]={0,0,0,0,0};
float roll_5s[5]={0,0,0,0,0};
float yaw_5s[5]={0,0,0,0,0};

int pencacahArray = 0;

struct MyData {
  byte X;
  byte Y;
  byte Z;
};

MyData data;

// Update these with values suitable for your network.
const char *ssid = "Kazarach IP";
const char *password = "modalcok";
const char *mqtt_server = "172.20.10.4";  // test.mosquitto.org
const int mqtt_port = 1883;


WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE (50)
char msg[MSG_BUFFER_SIZE];
int value = 0;


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
}

void accelerometer() {
  adampu.getEvent(&a, &g, &temp);
  // Get current acceleration values
  accX = a.acceleration.x;
  accY = a.acceleration.y;
  accZ = a.acceleration.z;
}

void degree() {
  // Baca data dari MPU6050
  int16_t ax, ay, az, gx, gy, gz;
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  // Konversi data gyro menjadi derajat per detik
  float gyroRate_pitch = (float)gx / 131.0;  // 131 LSB per deg/s
  float gyroRate_roll = (float)gy / 131.0;   // 131 LSB per deg/s
  float gyroRate_yaw = (float)gz / 131.0;    // 131 LSB per deg/s

  // Prediksi sudut berdasarkan rate gyro untuk setiap sumbu
  float dt = 0.01;  // Interval waktu (waktu sampling) dalam detik
  angle_pitch += dt * (gyroRate_pitch - bias_pitch);
  angle_roll += dt * (gyroRate_roll - bias_roll);
  angle_yaw += dt * (gyroRate_yaw - bias_yaw);

  // Update Covariance Matrix (P) untuk setiap sumbu
  P_pitch[0][0] += dt * (dt * P_pitch[1][1] - P_pitch[0][1] - P_pitch[1][0] + Q_angle);
  P_pitch[0][1] -= dt * P_pitch[1][1];
  P_pitch[1][0] -= dt * P_pitch[1][1];
  P_pitch[1][1] += Q_bias * dt;

  P_roll[0][0] += dt * (dt * P_roll[1][1] - P_roll[0][1] - P_roll[1][0] + Q_angle);
  P_roll[0][1] -= dt * P_roll[1][1];
  P_roll[1][0] -= dt * P_roll[1][1];
  P_roll[1][1] += Q_bias * dt;

  P_yaw[0][0] += dt * (dt * P_yaw[1][1] - P_yaw[0][1] - P_yaw[1][0] + Q_angle);
  P_yaw[0][1] -= dt * P_yaw[1][1];
  P_yaw[1][0] -= dt * P_yaw[1][1];
  P_yaw[1][1] += Q_bias * dt;

  // Kalman Gain untuk setiap sumbu
  float K_pitch[2];
  K_pitch[0] = P_pitch[0][0] / (P_pitch[0][0] + R_measure);
  K_pitch[1] = P_pitch[1][0] / (P_pitch[0][0] + R_measure);

  float K_roll[2];
  K_roll[0] = P_roll[0][0] / (P_roll[0][0] + R_measure);
  K_roll[1] = P_roll[1][0] / (P_roll[0][0] + R_measure);

  float K_yaw[2];
  K_yaw[0] = P_yaw[0][0] / (P_yaw[0][0] + R_measure);
  K_yaw[1] = P_yaw[1][0] / (P_yaw[0][0] + R_measure);

  // Update sudut berdasarkan pengukuran (accelerometer) untuk setiap sumbu
  float accAngle_pitch = atan2(ay, az) * RAD_TO_DEG;  // Menggunakan atan2 untuk mendapatkan sudut dari accelerometer
  float error_pitch = accAngle_pitch - angle_pitch;
  angle_pitch += K_pitch[0] * error_pitch;
  bias_pitch += K_pitch[1] * error_pitch;

  float accAngle_roll = atan2(ax, az) * RAD_TO_DEG;
  float error_roll = accAngle_roll - angle_roll;
  angle_roll += K_roll[0] * error_roll;
  bias_roll += K_roll[1] * error_roll;

  float accAngle_yaw = atan2(ay, ax) * RAD_TO_DEG;
  float error_yaw = accAngle_yaw - angle_yaw;
  angle_yaw += K_yaw[0] * error_yaw;
  bias_yaw += K_yaw[1] * error_yaw;

  // Update Covariance Matrix (P) untuk setiap sumbu
  float P00_temp_pitch = P_pitch[0][0];
  float P01_temp_pitch = P_pitch[0][1];

  P_pitch[0][0] -= K_pitch[0] * P00_temp_pitch;
  P_pitch[0][1] -= K_pitch[0] * P01_temp_pitch;
  P_pitch[1][0] -= K_pitch[1] * P00_temp_pitch;
  P_pitch[1][1] -= K_pitch[1] * P01_temp_pitch;

  float P00_temp_roll = P_roll[0][0];
  float P01_temp_roll = P_roll[0][1];

  P_roll[0][0] -= K_roll[0] * P00_temp_roll;
  P_roll[0][1] -= K_roll[0] * P01_temp_roll;
  P_roll[1][0] -= K_roll[1] * P00_temp_roll;
  P_roll[1][1] -= K_roll[1] * P01_temp_roll;

  float P00_temp_yaw = P_yaw[0][0];
  float P01_temp_yaw = P_yaw[0][1];

  P_yaw[0][0] -= K_yaw[0] * P00_temp_yaw;
  P_yaw[0][1] -= K_yaw[0] * P01_temp_yaw;
  P_yaw[1][0] -= K_yaw[1] * P00_temp_yaw;
  P_yaw[1][1] -= K_yaw[1] * P01_temp_yaw;
}

void publish() {

  // Serial.println(gyroX_5s);
  snprintf(msg, MSG_BUFFER_SIZE, "1 %.2f", gyroX_5s);
  client.publish("Arduino/GYRO X |", msg);

  // Serial.println(gyroY_5s);
  snprintf(msg, MSG_BUFFER_SIZE, "2 %.2f", gyroY_5s);
  client.publish("Arduino/GYRO Y |", msg);

  // Serial.println(gyroZ_5s);
  snprintf(msg, MSG_BUFFER_SIZE, "3 %.2f", gyroZ_5s);
  client.publish("Arduino/GYRO Z |", msg);

  // Serial.println(accX_5s);
  snprintf(msg, MSG_BUFFER_SIZE, "4 %.2f", accX_5s);
  client.publish("Arduino/ACC X |", msg);

  // Serial.println(accY_5s);
  snprintf(msg, MSG_BUFFER_SIZE, "5 %.2f", accY_5s);
  client.publish("Arduino/ACC Y |", msg);

  // Serial.println(accZ_5s);
  snprintf(msg, MSG_BUFFER_SIZE, "6 %.2f", accZ_5s);
  client.publish("Arduino/ACC Z |", msg);

  // Serial.println(pitch_5s);
  snprintf(msg, MSG_BUFFER_SIZE, "7 %.2f", pitch_5s);
  client.publish("Arduino/P |", msg);

  // Serial.println(roll_5s);
  snprintf(msg, MSG_BUFFER_SIZE, "8 %.2f", roll_5s);
  client.publish("Arduino/R |", msg);

  // Serial.println(yaw_5s);
  snprintf(msg, MSG_BUFFER_SIZE, "9 %.2f", yaw_5s);
  client.publish("Arduino/Y |", msg);
}

void monitoring() {
  Serial.println("GYROSCOPE");
  Serial.print("X = ");
  Serial.print(gyroX);
  Serial.print(" rad/s  |");
  Serial.print("Y = ");
  Serial.print(gyroY);
  Serial.print(" rad/s  |");

  Serial.print("Z = ");
  Serial.print(gyroZ);
  Serial.println(" rad/s");


  Serial.println("ACCELEROMETER");
  Serial.print("X = ");
  Serial.print(accX);
  Serial.print(" m/s2  |");

  Serial.print("Y = ");
  Serial.print(accY);
  Serial.print(" m/s2  |");

  Serial.print("Z = ");
  Serial.print(accZ);
  Serial.println(" m/s2");


  Serial.print("P : ");
  Serial.print(angle_pitch);

  Serial.print(" | R : ");
  Serial.print(angle_roll);

  Serial.print(" | Y : ");
  Serial.println(angle_yaw);
}
void saving_data() {
  File dataFile = SD.open("data.txt", FILE_WRITE);
  if (dataFile) {
    dataFile.printf("%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n", gyroX, gyroY, gyroZ, accX, accY, accZ, angle_pitch, angle_roll, angle_yaw);
    dataFile.close();
  }

  gyroX_5s[pencacahArray] = gyroX;
  gyroY_5s[pencacahArray] = gyroY;
  gyroZ_5s[pencacahArray] = gyroZ;

  accX_5s[pencacahArray] = accX;
  accY_5s[pencacahArray] = accY;
  accZ_5s[pencacahArray] = accZ;

  pitch_5s[pencacahArray] = angle_pitch;
  roll_5s[pencacahArray] = angle_roll;
  yaw_5s[pencacahArray] = angle_yaw;
  pencacahArray += 1;
  if (pencacahArray = 5) {
    pencacahArray = 0;
    for (int i = 0; i < 5; i++) {
      gyroX_5s[i] = 0;
      gyroY_5s[i] = 0;
      gyroZ_5s[i] = 0;

      accX_5s[i] = 0;
      accY_5s[i] = 0;
      accZ_5s[i] = 0;

      pitch_5s[i] = 0;
      roll_5s[i] = 0;
      yaw_5s[i] = 0;
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 12560);
  if (!SD.begin(chipSelect)) {
    Serial.println("Kartu microSD tidak terdeteksi!");
    return;
  }
  Serial.println("Kartu microSD terdeteksi!");
  SD.remove("data.txt");
  Wire.begin();
  mpu.initialize();
  adampu.begin();
  // Atur nilai awal state dan P untuk setiap sumbu
  angle_pitch = 0;
  bias_pitch = 0;
  P_pitch[0][0] = 0;
  P_pitch[0][1] = 0;
  P_pitch[1][0] = 0;
  P_pitch[1][1] = 0;

  angle_roll = 0;
  bias_roll = 0;
  P_roll[0][0] = 0;
  P_roll[0][1] = 0;
  P_roll[1][0] = 0;
  P_roll[1][1] = 0;

  angle_yaw = 0;
  bias_yaw = 0;
  P_yaw[0][0] = 0;
  P_yaw[0][1] = 0;
  P_yaw[1][0] = 0;
  P_yaw[1][1] = 0;
}


void loop() {
  unsigned long currentMillis = millis();  // Mendapatkan waktu saat ini

  // // Delay pertama
  // if (currentMillis - previousMillis1 >= interval1) {
  //   // Menyimpan waktu terakhir delay 1
  //   previousMillis1 = currentMillis;
  //   if (!client.connected()) {
  //     reconnect();
  //   }
  //   client.loop();
  // }

  // Delay kedua
  if (currentMillis - previousMillis2 >= interval2) {
    previousMillis2 = currentMillis;  // Menyimpan waktu terakhir delay 2

    gyroScope();
    accelerometer();
    degree();
    saving_data();
  }
  if (currentMillis - previousMillis3 >= interval3) {
    previousMillis3 = currentMillis;  // Menyimpan waktu terakhir delay 3
    monitoring();
    publish();
  }
}
