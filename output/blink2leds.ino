int led_principal = 13;int led_secundario = 2;int delay_longo = 2000;int delay_curto = 1000;
void setup() {
  pinMode(led_principal, OUTPUT);
  pinMode(led_secundario, OUTPUT);
}

void loop() {
  digitalWrite(led_principal, HIGH);
  digitalWrite(led_secundario, LOW);
  delay(delay_longo);
  digitalWrite(led_principal, LOW);
  digitalWrite(led_secundario, HIGH);
  delay(delay_curto);
}
