const int ledPin =11;
//Teensy 2.0 has the LED on pin 11
//Teensy++ 2.0 has the LED on pin 6
//Teensy 3.x has the LED on pin 13

//the setup() method runs once, when the sketch starts
void setup(){
  //initialize the digital pin as an output
  pinMode(ledPin, OUTPUT);
}

//the loop() method runs over and over again
//as long as the board has power

void loop(){
  digitalWrite(ledPin, HIGH); //set the LED on
  delay(1000); //wait for a second
  digitalWrite(ledPin, LOW); //set the LED off
  delay(1000); //wait for a second
}