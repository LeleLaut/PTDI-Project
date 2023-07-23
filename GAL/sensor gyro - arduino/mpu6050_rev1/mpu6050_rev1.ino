#include <Wire.h>       
#include <I2Cdev.h>     
#include <Adafruit_MPU6050.h>

#define triggerPin 4
#define echoPin 3
float cm = 0;

Adafruit_MPU6050 mpu;
int16_t ax, ay, az;
int16_t gx, gy, gz;
sensors_event_t a, g, temp;

//Gyroscope sensor deviation
float gyroXerror = 0.07;
float gyroYerror = 0.03;
float gyroZerror = 0.01;

float gyroX, gyroY, gyroZ;
float accX, accY, accZ;

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
  mpu.begin();
  //pinMode(LED_BUILTIN, OUTPUT);
}

void gyroScope()
{
  mpu.getEvent(&a, &g, &temp);

  float gyroX_temp = g.gyro.x;
  if(abs(gyroX_temp) > gyroXerror)  {
    gyroX += gyroX_temp/50.00;
  }
  
  float gyroY_temp = g.gyro.y;
  if(abs(gyroY_temp) > gyroYerror) {
    gyroY += gyroY_temp/70.00;
  }

  float gyroZ_temp = g.gyro.z;
  if(abs(gyroZ_temp) > gyroZerror) {
    gyroZ += gyroZ_temp/90.00;
  }
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
}

void accelerometer()
{
  mpu.getEvent(&a, &g, &temp);
  // Get current acceleration values
  accX = a.acceleration.x;
  accY = a.acceleration.y;
  accZ = a.acceleration.z;
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

}

long readUltrasonicDistance() {
  pinMode(triggerPin, OUTPUT);
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);
  pinMode(echoPin, INPUT);
  return pulseIn(echoPin, HIGH);
}

void loop()
{
  gyroScope();
  accelerometer();
  cm = 0.01723 * readUltrasonicDistance();
  Serial.println("HEIGHT");
  Serial.print(cm);
  Serial.println(" cm ");
  Serial.println(" ");
  delay(1500);
}
