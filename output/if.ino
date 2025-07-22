int temperatura = 35;int limite = 30;
void setup() {
  Serial.begin(9600);
}

void loop() {
  if (temperatura > limite) {
    Serial.println("ALERTA: Temperatura muito alta!");
  } else {
    Serial.println("Temperatura dboa.");
  }
  delay(5000);
}
