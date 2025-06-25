#include <Arduino.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

#include "my_func.h"

#define LED_PIN 2

Adafruit_MPU6050 mpu;

hw_timer_t *timer = NULL;
volatile SemaphoreHandle_t timerSemaphore;
portMUX_TYPE timerMux = portMUX_INITIALIZER_UNLOCKED;

void ARDUINO_ISR_ATTR onTimer()
{
  
  portENTER_CRITICAL_ISR(&timerMux);

  portEXIT_CRITICAL_ISR(&timerMux);
  // Give a semaphore that we can check in the loop
  xSemaphoreGiveFromISR(timerSemaphore, NULL);
  // It is safe to use digitalRead/Write here if you want to toggle an output
  digitalWrite(LED_PIN, !digitalRead(LED_PIN));
}

void setup()
{
    // inicializando seril comm
    Serial.begin(115200);

    // inicializando MPU
    mpu.begin();

    // configura MPU
    mpu.setSampleRateDivisor(0x07);
    mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
    mpu.setGyroRange(MPU6050_RANGE_250_DEG);
    

    // Create semaphore to inform us when the timer has fired
    timerSemaphore = xSemaphoreCreateBinary();

    // Set timer frequency to 1Mhz
    timer = timerBegin(0, 80, true);

    // Attach onTimer function to our timer.
    timerAttachInterrupt(timer, &onTimer, true);

    // Set alarm to call onTimer function every second (value in microseconds).
    // Repeat the alarm (third parameter) with unlimited count = 0 (fourth parameter).
    timerAlarmWrite(timer, 2000, true);
    timerAlarmEnable(timer);

}

void loop()
{
    if(xSemaphoreTake(timerSemaphore, 0) == pdTRUE)
    {
      sensors_event_t a, g, temp;
      mpu.getEvent(&a, &g, &temp);

      float acc[3] = {0};
      float gyr[3] = {0};

      portENTER_CRITICAL(&timerMux);
      
      portEXIT_CRITICAL(&timerMux);

      acc[0] = a.acceleration.x;
      acc[1] = a.acceleration.y;
      acc[2] = a.acceleration.z;

      gyr[0] = g.gyro.x;
      gyr[1] = g.gyro.y;
      gyr[2] = g.gyro.z;

      char sendData[26];
      en_pack('a', sendData, acc, gyr);

      Serial.print(sendData);
    }
}