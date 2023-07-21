#define triggerPin 4
#define echoPin 3
float cm = 0;

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

void setup() {
  Serial.begin(9600);
}

void loop() {
  cm = 0.01723 * readUltrasonicDistance();
  Serial.print(cm);
  Serial.println(" cm |");
  delay(500);
}
