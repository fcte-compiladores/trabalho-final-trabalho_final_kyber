String mensagem = "Tipos primitos!";int led_pin = 13;int tempo300 = 300;int tempo700 = 700;
void setup() {
  Serial.begin(9600);
  pinMode(led_pin, OUTPUT);
  Serial.println(mensagem);
}

void loop() {
  Serial.println("Ligando...");
  digitalWrite(led_pin, HIGH);
  delay(tempo300);
  Serial.println("Desligando...");
  digitalWrite(led_pin, LOW);
  delay(tempo700);
}
