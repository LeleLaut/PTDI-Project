#include <Wire.h>
#include <MPU6050_light.h>

MPU6050 mpu(Wire);

// Kalman Filter parameters
double Q_angle = 0.01;   // Process noise covariance for the accelerometer
double Q_gyro = 0.01;    // Process noise covariance for the gyroscope
double R_angle = 0.01;    // Measurement noise covariance

double angleX, angleY, angleZ; // Filtered angles

double P[2][2] = {
  { 1, 0 },
  { 0, 1 }
};

double K[2]; // Kalman gain

void setup() {
  Serial.begin(9600);
  Wire.begin();
  mpu.begin();
  Serial.println(F("Calculating gyro offset, do not move MPU6050"));
  mpu.calcGyroOffsets();
}

void loop() {
  mpu.update();

  double gyroRateX = mpu.getGyroX();
  double gyroRateY = mpu.getGyroY();
  double accAngleX = atan2(mpu.getAccY(), mpu.getAccZ()) * RAD_TO_DEG;
  double accAngleY = atan2(-mpu.getAccX(), mpu.getAccZ()) * RAD_TO_DEG;

  double dt = 0.1; // Time interval in seconds (adjust as needed)

  // Predicted angle (from gyro)
  angleX += gyroRateX * dt;
  angleY += gyroRateY * dt;

  // Kalman gain calculation
  double S = P[0][0] + R_angle;
  K[0] = P[0][0] / S;
  K[1] = P[1][0] / S;

  // Update angle estimates with Kalman filtered values
  angleX += K[0] * (accAngleX - angleX);
  angleY += K[0] * (accAngleY - angleY);

  // Update covariance matrix P
  P[0][0] -= K[0] * P[0][0];
  P[0][1] -= K[0] * P[0][1];
  P[1][0] -= K[1] * P[0][0];
  P[1][1] -= K[1] * P[0][1];

  Serial.print("P : ");
  Serial.print(angleX);
  Serial.print(" | R : ");
  Serial.print(angleY);
  Serial.print(" | Y : ");
  Serial.println(mpu.getAngleZ() * -1);
  
  delay(100);
}
