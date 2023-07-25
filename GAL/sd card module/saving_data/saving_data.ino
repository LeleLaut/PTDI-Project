#include <SPI.h>
#include <SD.h>
String logdata=""
const int chipSelect = 10; // Sesuaikan dengan pin Chip Select yang Anda gunakan

void setup() {
  Serial.begin(9600);
  
  // Inisialisasi kartu microSD
  if (!SD.begin(chipSelect)) {
    Serial.println("Kartu microSD tidak terdeteksi!");
    return;
  }
  Serial.println("Kartu microSD terdeteksi!");

 
}

void loop() {
  logdata=""
  File dataFile = SD.open("data.txt", FILE_WRITE);
  if (dataFile) {
    dataFile.println("Ini adalah contoh data yang ditulis ke berkas.");
    dataFile.close();
    Serial.println("Berhasil menulis data ke berkas data.txt.");
  } else {
    Serial.println("Gagal membuat atau membuka berkas data.txt.");
  }
}
