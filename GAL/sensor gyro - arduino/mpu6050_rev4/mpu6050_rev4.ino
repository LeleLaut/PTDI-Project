#include <Wire.h>
#include <MPU6050_light.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

MPU6050 mpu(Wire);

const float alpha = 0.4;  // Smoothing factor (adjust as needed)

float smoothedAngleX = 0.0;
float smoothedAngleY = 0.0;
float smoothedAngleZ = 0.0;

void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  Wire.begin();
  mpu.begin();
  Serial.println(F("Calculating gyro offset, do not move MPU6050"));
  mpu.calcGyroOffsets();  // the calibration
}

void loop() {
  mpu.update();

  // Read raw tilt angles
  float rawAngleX = mpu.getAngleX();
  float rawAngleY = mpu.getAngleY();
  float rawAngleZ = mpu.getAngleZ();

  // Apply exponential moving average filter
  smoothedAngleX = (alpha * rawAngleX) + ((1 - alpha) * smoothedAngleX);
  smoothedAngleY = (alpha * rawAngleY) + ((1 - alpha) * smoothedAngleY);
  smoothedAngleZ = ((alpha * rawAngleZ) + ((1 - alpha) * smoothedAngleZ)) * -1;

  // Get rotation angle on Z axis

  // Print the smoothed angles
  Serial.print("P : ");
  Serial.print(smoothedAngleX);
  Serial.print(" | R : ");
  Serial.print(smoothedAngleY);

  lcd.setCursor(0, 0);
  lcd.printf("%.2f %.2f", smoothedAngleX, smoothedAngleY);

  delay(500);
  lcd.clear();
}
