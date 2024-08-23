const int ledPin = 11;
const int soilPin = 20;
// the setup() method runs once, when the sketch starts
void setup() {
  // initialize the digital pin as an output.
  pinMode(ledPin, OUTPUT);
  Serial.begin(9800);
}
void loop() {
  int val = analogRead(soilPin);
  Serial.print("Soil : ");
  Serial.println(val);
  digitalWrite(ledPin, HIGH); // set the LED on
  delay(1000); // wait for a second
  digitalWrite(ledPin, LOW); // set the LED off
  delay(100); // wait for a second
}

