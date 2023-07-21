#include <Wire.h>
#include <ESP8266WiFi.h>
#include <Adafruit_MPU6050.h>

// Konfigurasi WiFi
const char* ssid = "GAL";
const char* password = "gaadayangtau";

// Inisialisasi objek MPU6050
Adafruit_MPU6050 mpu;

void setup() {
  // Mulai komunikasi serial
  Serial.begin(9600);

  // Mulai komunikasi I2C
  Wire.begin();

  // Hubungkan ke jaringan WiFi
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");

  // Inisialisasi MPU6050
  mpu.initialize();

  // Cek koneksi MPU6050
  Serial.println(mpu.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");
}

void loop() {
  // Baca data akselerometer dan giroskop
  int16_t ax, ay, az, gx, gy, gz;
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  // Tampilkan data di Serial Monitor
  Serial.print("Accelerometer (g): ");
  Serial.print(ax / 16384.0);
  Serial.print(", ");
  Serial.print(ay / 16384.0);
  Serial.print(", ");
  Serial.print(az / 16384.0);
  Serial.print(" | ");

  Serial.print("Gyroscope (°/s): ");
  Serial.print(gx / 131.0);
  Serial.print(", ");
  Serial.print(gy / 131.0);
  Serial.print(", ");
  Serial.println(gz / 131.0);

  delay(500);  // Delay antar pembacaan
}
