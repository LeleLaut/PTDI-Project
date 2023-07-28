// #include <Wire.h>
// #include <MPU6050_light.h>

// MPU6050 mpu(Wire);

// const float alpha = 0.98; // Parameter smoothing untuk menggabungkan data accelerometer dan gyroscope
// float angleZ = 0; // Sudut rotasi pada sumbu Z

// void setup() {
//   Serial.begin(9600);                                                
//   Wire.begin();
//   mpu.begin();
//   Serial.println(F("Calculating gyro offset, do not move MPU6050"));       
//   mpu.calcGyroOffsets();                           // the calibration        
// }

// void loop() {
//   mpu.update();   
  
//   // Mendapatkan sudut rotasi dari gyroscope (raw value)
//   float gyroZ = mpu.getAngleZ();
  
//   // Mendapatkan sudut rotasi dari accelerometer
//   float accZ = atan2(mpu.getAccY(), mpu.getAccX()) * RAD_TO_DEG;
  
//   // Menggabungkan data gyroscope dan accelerometer untuk mengoreksi drift
//   angleZ = alpha * (angleZ + gyroZ * 0.01) + (1 - alpha) * accZ;
  
//   Serial.print("Corrected Yaw : ");
//   Serial.println(angleZ);                
//   delay(100);
// }




// #include <Wire.h>
// #include <MPU6050_light.h>

// MPU6050 mpu(Wire);

// const int numReadings = 5; // Jumlah pembacaan untuk Moving Average Filter
// float readingsX[numReadings];
// float readingsY[numReadings];
// float readingsZ[numReadings];
// int currentIndex = 0;

// void setup() {
//   Serial.begin(9600);                                                
//   Wire.begin();
//   mpu.begin();
//   Serial.println(F("Calculating gyro offset, do not move MPU6050"));       
//   mpu.calcGyroOffsets();                           // the calibration        
// }

// void loop() {
//   mpu.update();   
  
//   // Mendapatkan data dari sensor
//   float angleX = mpu.getAngleX();
//   float angleY = mpu.getAngleY();
//   float angleZ = mpu.getAngleZ() * -1;
  
//   // Memasukkan data ke dalam array untuk Moving Average Filter
//   readingsX[currentIndex] = angleX;
//   readingsY[currentIndex] = angleY;
//   readingsZ[currentIndex] = angleZ;
//   currentIndex = (currentIndex + 1) % numReadings;
  
//   // Menghitung rata-rata dari data dalam array
//   float avgX = 0;
//   float avgY = 0;
//   float avgZ = 0;
//   for (int i = 0; i < numReadings; i++) {
//     avgX += readingsX[i];
//     avgY += readingsY[i];
//     avgZ += readingsZ[i];
//   }
//   avgX /= numReadings;
//   avgY /= numReadings;
//   avgZ /= numReadings;
  
//   Serial.print("Filtered P : ");
//   Serial.print(avgX);
//   Serial.print(" | Filtered R : ");
//   Serial.print(avgY);
//   Serial.print(" | Filtered Y : ");
//   Serial.println(avgZ);
  
//   delay(100);
// }




