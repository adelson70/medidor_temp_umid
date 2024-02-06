#include <DHT.h>

#define DHT_PIN 2 
#define DHT_TYPE DHT11 

DHT dht(DHT_PIN, DHT_TYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  int tempo = (2*1000);
  delay(tempo); // espera 2 segundos para nova leitura
  
  float temperatura = dht.readTemperature();
  float umidade = dht.readHumidity();
  
  if (isnan(temperatura) || isnan(umidade)) {
    Serial.println("Falha ao ler o sensor DHT!");
    return;
  }

  Serial.print(temperatura);
  Serial.print(";");
  Serial.print(umidade);
  
}
