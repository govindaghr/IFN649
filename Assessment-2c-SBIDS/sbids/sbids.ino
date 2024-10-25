#include <DHT.h>
#include <SoftwareSerial.h>

// Define pins
// #define SHOCK_SENSOR_PIN 2
#define REED_SWITCH_PIN 3
#define DHT_PIN 21
#define BUZZER_PIN 5

// Initialize DHT sensor
#define DHTTYPE DHT11
DHT dht(DHT_PIN, DHTTYPE);

bool alarmTriggered = false;
bool sensorsActive = true;
unsigned long previousMillis = 0;
const long tempInterval = 30000;  // 30 seconds in milliseconds

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600); // Initialize Serial1 for Bluetooth

  // Initialize sensors
  pinMode(SHOCK_SENSOR_PIN, INPUT);
  pinMode(REED_SWITCH_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  dht.begin();
}

void loop() {
  unsigned long currentMillis = millis();

  // Check for Bluetooth commands
  if (Serial1.available()) {
    String btCommand = Serial1.readStringUntil('\n');
    btCommand.trim();
    Serial.println(btCommand);
    if (btCommand == "RESET") {
      resetAlarm();
    } else if (btCommand == "OPEN") {
      sensorsActive = false;
      Serial.println("Sensors deactivated.");
      Serial1.println("Sensors deactivated.");
    } else if (btCommand == "CLOSE") {
      sensorsActive = true;
      Serial.println("Sensors activated.");
      Serial1.println("Sensors activated.");
    }
  }

  if (sensorsActive) {
    // Read reed switch
    int reedValue = digitalRead(REED_SWITCH_PIN);
    Serial.print("Reed Switch Value: ");
    Serial.println(reedValue);

    if (reedValue == LOW && !alarmTriggered) {
      triggerAlarm("UnauthorizedAccess");
    }

    // Check if it's time to send temperature and humidity data
    if (currentMillis - previousMillis >= tempInterval) {
      previousMillis = currentMillis;

      // Read temperature and humidity from DHT11
      float temperature = dht.readTemperature();
      float humidity = dht.readHumidity();
      if (isnan(temperature) || isnan(humidity)) {
        Serial.println("Failed to read from DHT sensor!");
      } else {
        String tempMessage = "Temperature: " + String(temperature) + " C, Humidity: " + String(humidity) + " %";
        Serial.println(tempMessage);
        Serial1.println(tempMessage); // Send to Bluetooth
      }
    }
  }

  delay(1000); // Short sleep for reed switch
}

void triggerAlarm(String message) {
  Serial.println(message);
  Serial1.println(message);
  digitalWrite(BUZZER_PIN, HIGH);
  alarmTriggered = true;
}

void resetAlarm() {
  Serial.println("Alarm reset.");
  Serial1.println("Alarm reset.");
  digitalWrite(BUZZER_PIN, LOW);
  alarmTriggered = false;
}
