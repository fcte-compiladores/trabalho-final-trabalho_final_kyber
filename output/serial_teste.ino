int contador = 0;String mensagem_inicial = "Cristal Kyber Verde!";
void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  Serial.println(mensagem_inicial);
}

void loop() {
  Serial.println("LED Aceso");
  digitalWrite(13, HIGH);
  delay(1000);
  Serial.println("LED Apagado");
  digitalWrite(13, LOW);
  delay(1000);
}
