int blink_delay = 500;int led_pin = 13;
void setup() {
  pinMode(led_pin, OUTPUT);
}

void loop() {
  digitalWrite(led_pin, HIGH);
  delay(blink_delay);
  digitalWrite(led_pin, LOW);
  delay(blink_delay);
}
