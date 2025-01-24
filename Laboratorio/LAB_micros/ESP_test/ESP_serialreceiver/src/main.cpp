#include <Arduino.h>

#define LED_PIN 2

void fromFloatToBytes(byte* , float);
float fromBytesToFloat(byte*);
void find_sep(byte*, byte*, char*);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  char myData[10] = {0};
  char sendData[9];
  byte s1[4];
  byte s2[4];

  float f1;
  float f2;
  
  if(Serial.available() > 0)
  {
    digitalWrite(LED_PIN, HIGH);
    byte m = Serial.readBytesUntil('\n', myData, 30);
    //extrayendo partes
    find_sep(s1, s2, myData);
    
    //operaciones
    f1 = fromBytesToFloat(s1);
    f1 = f1 * 0.45;

    f2 = fromBytesToFloat(s2);
    f2 = f2 * 0.55;

    // a bytes para enviar
    fromFloatToBytes(s1, f1);
    fromFloatToBytes(s2,f2);

    // Al buffer de atos de envio
    sendData[0] =s1[0];
    sendData[1] =s1[1];
    sendData[2] =s1[2];
    sendData[3] =s1[3];
    sendData[4] =s2[0];
    sendData[5] =s2[1];
    sendData[6] =s2[2];
    sendData[7] =s2[3];
    sendData[8] = '\n';
    // Enviando
    Serial.write(sendData,9);

    digitalWrite(LED_PIN, LOW);
  }
}

//De bytes a float
float fromBytesToFloat(byte* packet)
{
  float f;
  memcpy(&f, packet, sizeof(f));
  return f;
}

void fromFloatToBytes(byte* bytes, float f)
{
  int length = sizeof(float);
  for(int i = 0; i<length; i++)
  {
    bytes[i] = ((byte*)&f)[i];
  }
}

void find_sep(byte* buf1, byte* buf2, char* cad)
{
  
  for(byte i; i<4; i++)
  {
    buf1[i] = (byte)cad[i];
    buf2[i] = (byte)cad[i+5];
  }
}