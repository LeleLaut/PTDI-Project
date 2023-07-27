/* Get tilt angles on X and Y, and rotation angle on Z
 * 
 * License: MIT
 */

#include <Wire.h>
#include <MPU6050_light.h>

MPU6050 mpu(Wire);

void setup() {
  Serial.begin(9600);                                                
  Wire.begin();
  mpu.begin();
  Serial.println(F("Calculating gyro offset, do not move MPU6050"));       
  mpu.calcGyroOffsets();                           // the calibration        
}

void loop() {
  mpu.update();   
  Serial.print("P : ");
  Serial.print(mpu.getAngleX());
  Serial.print(" | R : ");
  Serial.print(mpu.getAngleY());
  Serial.print(" | Y : ");
  Serial.println(mpu.getAngleZ() * -1);                
  delay(100);
}