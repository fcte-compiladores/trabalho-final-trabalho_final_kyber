
void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  Serial.println("Kyber iniciado! Teste de serial e LED.");
}

void loop() {
  Serial.println("loop");
  digitalWrite(13, HIGH);
  Serial.println("LED Aceso");
  delay(500);
  digitalWrite(13, LOW);
  Serial.println("LED Apagado");
  delay(500);
}

