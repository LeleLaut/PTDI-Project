#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <MPU6050.h>
#include <Adafruit_MPU6050.h>
#include <SPI.h>
#include <SD.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_HMC5883_U.h>
#include <WiFiUdp.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

#define I2C_SDA_PIN D2
#define I2C_SCL_PIN D1

Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345);
float yaw_offset = 0.0;  // Variabel untuk menyimpan nilai referensi yaw
float angle_yaw;

const unsigned long interval1 = 1000;  //penentu frekuensi
const unsigned long interval2 = 10;
const unsigned long interval3 = 5000;
const unsigned long interval4 = 100;
const unsigned int n = interval3 / interval1;

unsigned long previousMillis1 = 0;  // Menyimpan waktu terakhir delay 1
unsigned long previousMillis2 = 0;  // Menyimpan waktu terakhir delay 2
unsigned long previousMillis3 = 0;  // Menyimpan waktu terakhir delay 3
unsigned long previousMillis4 = 0;  // Menyimpan waktu terakhir delay 4

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
const float Q_angle = 0.1;    // Variance dari estimasi ketidakpastian sensor
const float Q_bias = 0.1;     // Variance dari estimasi ketidakpastian bias
const float R_measure = 0.1;  // Variance dari ketidakpastian pengukuran

// State Kalman Filter untuk setiap sumbu
float angle_pitch = 0;  // Sudut hasil estimasi Pitch
float angle_roll = 0;   // Sudut hasil estimasi Roll

float bias_pitch = 0;  // Bias hasil estimasi Pitch
float bias_roll = 0;   // Bias hasil estimasi Roll

float rate_pitch = 0;  // Derivatif sudut dari sensor Pitch
float rate_roll = 0;   // Derivatif sudut dari sensor Roll

// Posisi Covariance untuk setiap sumbu
float P_pitch[2][2] = { { 0, 0 }, { 0, 0 } };
float P_roll[2][2] = { { 0, 0 }, { 0, 0 } };

float gyroX_arr[n];
float gyroY_arr[n];
float gyroZ_arr[n];

float accX_arr[n];
float accY_arr[n];
float accZ_arr[n];

float pitch_arr[n];
float roll_arr[n];
float yaw_arr[n];

int pencacahArray = 0;
int counter_sdcard = 0;

// Update these with values suitable for your network.
const char* ssid = "KAZ";
const char* password = "modalcokla";
const char* mqtt_server = "test.mosquitto.org";  // test.mosquitto.org     0.tcp.ap.ngrok.io
const int mqtt_port = 1883;
unsigned int broadcastPort = 51111;  // UDP

WiFiUDP udp;

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE (200)
char msg[MSG_BUFFER_SIZE];


void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Connecting to: ");
  lcd.setCursor(0, 1);
  lcd.print(ssid);


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
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Connected to:");
  lcd.setCursor(0, 1);
  lcd.print(ssid);
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Connecting MQTT");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("MQTT Connected");
      // Once connected, publish an announcement...
      client.publish("device/temp", "MQTT Server is Connected");
      // ... and resubscribe
      client.subscribe("device/led");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("MQTT Failed");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void broadcasting() {
  // const char* broadcastData = "Hello from ESP8266!";
  udp.beginPacket(IPAddress(192, 168, 46, 191), broadcastPort);
  udp.printf("%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n", gyroX, gyroY, gyroZ, accX, accY, accZ, angle_pitch, angle_roll * -1, angle_yaw);
  udp.endPacket();
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

  sensors_event_t event;
  mag.getEvent(&event);

  // Konversi data gyro menjadi derajat per detik
  float gyroRate_pitch = (float)gx / 131.0;  // 131 LSB per deg/s
  float gyroRate_roll = (float)gy / 131.0;   // 131 LSB per deg/s

  // Prediksi sudut berdasarkan rate gyro untuk setiap sumbu
  float dt = 0.01;  // Interval waktu (waktu sampling) dalam detik
  angle_pitch += dt * (gyroRate_pitch - bias_pitch);
  angle_roll += dt * (gyroRate_roll - bias_roll);

  // Update Covariance Matrix (P) untuk setiap sumbu
  P_pitch[0][0] += dt * (dt * P_pitch[1][1] - P_pitch[0][1] - P_pitch[1][0] + Q_angle);
  P_pitch[0][1] -= dt * P_pitch[1][1];
  P_pitch[1][0] -= dt * P_pitch[1][1];
  P_pitch[1][1] += Q_bias * dt;

  P_roll[0][0] += dt * (dt * P_roll[1][1] - P_roll[0][1] - P_roll[1][0] + Q_angle);
  P_roll[0][1] -= dt * P_roll[1][1];
  P_roll[1][0] -= dt * P_roll[1][1];
  P_roll[1][1] += Q_bias * dt;

  // Kalman Gain untuk setiap sumbu
  float K_pitch[2];
  K_pitch[0] = P_pitch[0][0] / (P_pitch[0][0] + R_measure);
  K_pitch[1] = P_pitch[1][0] / (P_pitch[0][0] + R_measure);

  float K_roll[2];
  K_roll[0] = P_roll[0][0] / (P_roll[0][0] + R_measure);
  K_roll[1] = P_roll[1][0] / (P_roll[0][0] + R_measure);

  // Update sudut berdasarkan pengukuran (accelerometer) untuk setiap sumbu
  float accAngle_pitch = atan2(ay, az) * RAD_TO_DEG;  // Menggunakan atan2 untuk mendapatkan sudut dari accelerometer
  float error_pitch = accAngle_pitch - angle_pitch;
  angle_pitch += K_pitch[0] * error_pitch;
  bias_pitch += K_pitch[1] * error_pitch;

  float accAngle_roll = atan2(ax, az) * RAD_TO_DEG;
  float error_roll = accAngle_roll - angle_roll;
  angle_roll += K_roll[0] * error_roll;
  bias_roll += K_roll[1] * error_roll;

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

  float heading = atan2(event.magnetic.y, event.magnetic.x);
  if (heading < 0) heading += 2 * PI;

  float heading_deg = heading * 180 / PI;
  angle_yaw = heading_deg - yaw_offset;  // Menggunakan nilai referensi yaw

  // Normalisasi yaw ke dalam range 0 - 360 derajat
  if (angle_yaw < 0) {
    angle_yaw += 360;
  }

  // Serial.print("Yaw: ");
  // Serial.print(angle_yaw);
  // Serial.println(" degrees");
}

void publish() {
  char str_gyroX_arr[200];
  char* arrayStr_str_gyroX_arr = str_gyroX_arr;
  arrayStr_str_gyroX_arr += sprintf(arrayStr_str_gyroX_arr, "[");
  for (int i = 0; i < n; i++) {
    arrayStr_str_gyroX_arr += sprintf(arrayStr_str_gyroX_arr, "%.2f", gyroX_arr[i]);  // Use 2 decimal places
    if (i < n - 1) {
      arrayStr_str_gyroX_arr += sprintf(arrayStr_str_gyroX_arr, ", ");
    }
  }
  arrayStr_str_gyroX_arr += sprintf(arrayStr_str_gyroX_arr, "]");

  char str_gyroY_arr[200];
  char* arrayStr_str_gyroY_arr = str_gyroY_arr;
  arrayStr_str_gyroY_arr += sprintf(arrayStr_str_gyroY_arr, "[");
  for (int i = 0; i < n; i++) {
    arrayStr_str_gyroY_arr += sprintf(arrayStr_str_gyroY_arr, "%.2f", gyroY_arr[i]);  // Use 2 decimal places
    if (i < n - 1) {
      arrayStr_str_gyroY_arr += sprintf(arrayStr_str_gyroY_arr, ", ");
    }
  }
  arrayStr_str_gyroY_arr += sprintf(arrayStr_str_gyroY_arr, "]");

  char str_gyroZ_arr[200];
  char* arrayStr_str_gyroZ_arr = str_gyroZ_arr;
  arrayStr_str_gyroZ_arr += sprintf(arrayStr_str_gyroZ_arr, "[");
  for (int i = 0; i < n; i++) {
    arrayStr_str_gyroZ_arr += sprintf(arrayStr_str_gyroZ_arr, "%.2f", gyroZ_arr[i]);  // Use 2 decimal places
    if (i < n - 1) {
      arrayStr_str_gyroZ_arr += sprintf(arrayStr_str_gyroZ_arr, ", ");
    }
  }
  arrayStr_str_gyroZ_arr += sprintf(arrayStr_str_gyroZ_arr, "]");

  char str_accX_arr[200];
  char* arrayStr_str_accX_arr = str_accX_arr;
  arrayStr_str_accX_arr += sprintf(arrayStr_str_accX_arr, "[");
  for (int i = 0; i < n; i++) {
    arrayStr_str_accX_arr += sprintf(arrayStr_str_accX_arr, "%.2f", accX_arr[i]);  // Use 2 decimal places
    if (i < n - 1) {
      arrayStr_str_accX_arr += sprintf(arrayStr_str_accX_arr, ", ");
    }
  }
  arrayStr_str_accX_arr += sprintf(arrayStr_str_accX_arr, "]");

  char str_accY_arr[200];
  char* arrayStr_str_accY_arr = str_accY_arr;
  arrayStr_str_accY_arr += sprintf(arrayStr_str_accY_arr, "[");
  for (int i = 0; i < n; i++) {
    arrayStr_str_accY_arr += sprintf(arrayStr_str_accY_arr, "%.2f", accY_arr[i]);  // Use 2 decimal places
    if (i < n - 1) {
      arrayStr_str_accY_arr += sprintf(arrayStr_str_accY_arr, ", ");
    }
  }
  arrayStr_str_accY_arr += sprintf(arrayStr_str_accY_arr, "]");

  char str_accZ_arr[200];
  char* arrayStr_str_accZ_arr = str_accZ_arr;
  arrayStr_str_accZ_arr += sprintf(arrayStr_str_accZ_arr, "[");
  for (int i = 0; i < n; i++) {
    arrayStr_str_accZ_arr += sprintf(arrayStr_str_accZ_arr, "%.2f", accZ_arr[i]);  // Use 2 decimal places
    if (i < n - 1) {
      arrayStr_str_accZ_arr += sprintf(arrayStr_str_accZ_arr, ", ");
    }
  }
  arrayStr_str_accZ_arr += sprintf(arrayStr_str_accZ_arr, "]");

  char str_pitch_arr[200];
  char* arrayStr_str_pitch_arr = str_pitch_arr;
  arrayStr_str_pitch_arr += sprintf(arrayStr_str_pitch_arr, "[");
  for (int i = 0; i < n; i++) {
    arrayStr_str_pitch_arr += sprintf(arrayStr_str_pitch_arr, "%.2f", pitch_arr[i]);  // Use 2 decimal places
    if (i < n - 1) {
      arrayStr_str_pitch_arr += sprintf(arrayStr_str_pitch_arr, ", ");
    }
  }
  arrayStr_str_pitch_arr += sprintf(arrayStr_str_pitch_arr, "]");

  char str_roll_arr[200];
  char* arrayStr_str_roll_arr = str_roll_arr;
  arrayStr_str_roll_arr += sprintf(arrayStr_str_roll_arr, "[");
  for (int i = 0; i < n; i++) {
    arrayStr_str_roll_arr += sprintf(arrayStr_str_roll_arr, "%.2f", roll_arr[i]);  // Use 2 decimal places
    if (i < n - 1) {
      arrayStr_str_roll_arr += sprintf(arrayStr_str_roll_arr, ", ");
    }
  }
  arrayStr_str_roll_arr += sprintf(arrayStr_str_roll_arr, "]");

  char str_yaw_arr[200];
  char* arrayStr_str_yaw_arr = str_yaw_arr;
  arrayStr_str_yaw_arr += sprintf(arrayStr_str_yaw_arr, "[");
  for (int i = 0; i < n; i++) {
    arrayStr_str_yaw_arr += sprintf(arrayStr_str_yaw_arr, "%.2f", yaw_arr[i]);  // Use 2 decimal places
    if (i < n - 1) {
      arrayStr_str_yaw_arr += sprintf(arrayStr_str_yaw_arr, ", ");
    }
  }
  arrayStr_str_yaw_arr += sprintf(arrayStr_str_yaw_arr, "]");

  snprintf(msg, MSG_BUFFER_SIZE, "1 %s", str_gyroX_arr);
  client.publish("Arduino/GYRO X |", msg);

  snprintf(msg, MSG_BUFFER_SIZE, "2 %s", str_gyroY_arr);
  client.publish("Arduino/GYRO Y |", msg);

  snprintf(msg, MSG_BUFFER_SIZE, "3 %s", str_gyroZ_arr);
  client.publish("Arduino/GYRO Z |", msg);

  snprintf(msg, MSG_BUFFER_SIZE, "4 %s", str_accX_arr);
  client.publish("Arduino/ACC X |", msg);

  snprintf(msg, MSG_BUFFER_SIZE, "5 %s", str_accY_arr);
  client.publish("Arduino/ACC Y |", msg);

  snprintf(msg, MSG_BUFFER_SIZE, "6 %s", str_accZ_arr);
  client.publish("Arduino/ACC Z |", msg);

  snprintf(msg, MSG_BUFFER_SIZE, "7 %s", str_pitch_arr);
  client.publish("Arduino/P |", msg);

  snprintf(msg, MSG_BUFFER_SIZE, "8 %s", str_roll_arr);
  client.publish("Arduino/R |", msg);

  snprintf(msg, MSG_BUFFER_SIZE, "9 %s", str_yaw_arr);
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
  Serial.print(angle_pitch* -1);

  Serial.print(" | R : ");
  Serial.print(angle_roll);

  Serial.print(" | Y : ");
  Serial.println(angle_yaw);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.printf("%.2f %.2f", angle_pitch* -1, angle_roll);
  lcd.setCursor(0, 1);
  lcd.printf("%.2f", angle_yaw);
  lcd.setCursor(12, 1);
  lcd.printf("%d", counter_sdcard);
}

void saving_data() {
  File dataFile = SD.open("data.txt", FILE_WRITE);
  if (dataFile) {
    dataFile.printf("%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%d\n", gyroX, gyroY, gyroZ, accX, accY, accZ, angle_pitch* -1, angle_roll, angle_yaw, counter_sdcard);
    dataFile.close();
  }

  gyroX_arr[pencacahArray] = gyroX;
  gyroY_arr[pencacahArray] = gyroY;
  gyroZ_arr[pencacahArray] = gyroZ;

  accX_arr[pencacahArray] = accX;
  accY_arr[pencacahArray] = accY;
  accZ_arr[pencacahArray] = accZ;

  pitch_arr[pencacahArray] = angle_pitch* -1;
  roll_arr[pencacahArray] = angle_roll;
  yaw_arr[pencacahArray] = angle_yaw;

  Serial.println(counter_sdcard);
  counter_sdcard = counter_sdcard + 1;
  Serial.println(pencacahArray);
  pencacahArray += 1;

  if (pencacahArray > n) {
    pencacahArray = 0;
  }
}

void calibrateYaw() {
  float sum_yaw = 0;
  int num_samples = 200;  // Jumlah sampel untuk kalibrasi (dapat diatur sesuai kebutuhan)

  // Mengambil beberapa sampel yaw dan menghitung rata-rata
  for (int i = 0; i < num_samples; i++) {
    sensors_event_t event;
    mag.getEvent(&event);
    float heading = atan2(event.magnetic.y, event.magnetic.x);
    if (heading < 0) heading += 2 * PI;
    float heading_deg = heading * 180 / PI;
    sum_yaw += heading_deg;
    delay(5);  // Jeda 5 ms antara sampel
  }

  // Menghitung nilai rata-rata yaw sebagai referensi
  yaw_offset = sum_yaw / num_samples;
}

void setup() {
  Serial.begin(115200);
  lcd.init();       // initialize the lcd
  lcd.backlight();  // Turn on the LCD screen backlight
  lcd.setCursor(0, 0);
  lcd.print("Starting up!");
  setup_wifi();
  udp.begin(broadcastPort);
  client.setServer(mqtt_server, mqtt_port);
  if (!SD.begin(chipSelect)) {
    Serial.println("Kartu microSD tidak terdeteksi!");
    return;
  }
  Serial.println("Kartu microSD terdeteksi!");
  SD.remove("data.txt");
  Wire.begin(I2C_SDA_PIN, I2C_SCL_PIN);
  mpu.initialize();
  if (!mag.begin()) {
    Serial.println("Could not find a valid HMC5883L sensor, check wiring!");
    return;
  }

  Serial.println("HMC5883L sensor detected");

  // Menjalankan kalibrasi yaw saat program pertama kali dijalankan
  calibrateYaw();
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
}

void loop() {
  unsigned long currentMillis = millis();  // Mendapatkan waktu saat ini

  // thread 1
  if (currentMillis - previousMillis1 >= interval1) {
    // Menyimpan waktu terakhir delay 1
    previousMillis1 = currentMillis;
    if (!client.connected()) {
      reconnect();
    }
    client.loop();
    saving_data();
    monitoring();
    broadcasting();
  }

  // thread 2
  if (currentMillis - previousMillis2 >= interval2) {
    previousMillis2 = currentMillis;  // Menyimpan waktu terakhir delay 2
    gyroScope();
    accelerometer();
    degree();
  }

  // thread 3
  if (currentMillis - previousMillis3 >= interval3) {
    previousMillis3 = currentMillis;  // Menyimpan waktu terakhir delay 3
    publish();
  }

  // thread 4
  if (currentMillis - previousMillis4 >= interval4) {
    previousMillis4 = currentMillis;  // Menyimpan waktu terakhir delay 4
  }
}
