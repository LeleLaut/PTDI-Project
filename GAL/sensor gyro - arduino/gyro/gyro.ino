#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

void setup(){
  Serial.begin(115200);
  Serial.println("Initialize MPU6050");
  while(!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G)){
    Serial.println("Could not find a valid MPU6050 sensor, check wiring!");
    delay(500);
  }
  checkSettings();
}

void checkSettings(){
  Serial.println();
  Serial.println("*Sleep mode:       ");
  Serial.println(mpu.getSleepEnabled() ? "Enabled" : "Disabled");

  
}