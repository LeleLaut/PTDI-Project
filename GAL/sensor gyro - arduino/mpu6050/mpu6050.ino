#include <Wire.h>       
#include <I2Cdev.h>     
#include <MPU6050.h>    

MPU6050 mpu;
int16_t ax, ay, az;
int16_t gx, gy, gz;

struct MyData {
  byte X;
  byte Y;
  byte Z;
};

MyData data;

void setup()
{
  Serial.begin(9600);
  Wire.begin();
  mpu.initialize();
  //pinMode(LED_BUILTIN, OUTPUT);
}

void loop()
{
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  data.X = map(ax, -17000, 17000, -255, 255); // X axis data
  data.Y = map(ay, -17000, 17000, -180, 180); 
  data.Z = map(az, -17000, 17000, -180, 180);  // Y axis data
  delay(1000);
  Serial.print("Axis X1 = ");
  Serial.print(data.X);
  Serial.print("  ");
  Serial.print("Axis Y1 = ");
  Serial.print(data.Y);
  Serial.print("  ");
  Serial.print("Axis Z1 = ");
  Serial.println(data.Z);
}
