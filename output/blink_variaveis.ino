int blink_delay = 500;

void setup() {
  pinMode(13, OUTPUT);
}

void loop() {
  digitalWrite(13, HIGH);
  delay(blink_delay);
  digitalWrite(13, LOW);
  delay(blink_delay);
}

