#include <SPI.h>
#include <SD.h>

const int chipSelect = D5; // Gunakan pin CS yang Anda hubungkan ke modul microSD

void setup() {
  Serial.begin(9600);

  // Inisialisasi koneksi SPI dan kartu microSD
  if (!SD.begin(chipSelect)) {
    Serial.println("Kartu microSD tidak terdeteksi!");
    return;
  }
  Serial.println("Kartu microSD terdeteksi!");
}

void loop() {
  // Contoh penulisan data ke kartu microSD
  File dataFile = SD.open("data.txt", FILE_WRITE);
  if (dataFile) {
    dataFile.println("Ini adalah contoh data yang ditulis ke kartu microSD.");
    dataFile.close();
    Serial.println("Berhasil menulis data ke kartu microSD.");
  } else {
    Serial.println("Gagal menulis data ke kartu microSD.");
  }

  // Contoh membaca data dari kartu microSD
  File dataFile = SD.open("data.txt");
  if (dataFile) {
    while (dataFile.available()) {
      Serial.write(dataFile.read());
    }
    dataFile.close();
  } else {
    Serial.println("Gagal membaca data dari kartu microSD.");
  }

  delay(5000); // Tunggu 5 detik sebelum menulis/membaca ulang data
}
