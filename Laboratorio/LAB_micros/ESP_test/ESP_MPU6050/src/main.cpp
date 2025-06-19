#include <Arduino.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

#include "my_util.h"

Adafruit_MPU6050 mpu;

hw_timer_t *timer = NULL;
volatile SemaphoreHandle_t timerSemaphore;
portMUX_TYPE timerMux = portMUX_INITIALIZER_UNLOCKED;

volatile float acc_t[3] = {0};
volatile float gyr_t[3] = {0};

void ARDUINO_ISR_ATTR onTimer()
{
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  // Increment the counter and set the time of ISR
  portENTER_CRITICAL_ISR(&timerMux);
  acc_t[0] = a.acceleration.x;
  acc_t[1] = a.acceleration.y;
  acc_t[2] = a.acceleration.z;

  gyr_t[0] = g.gyro.x;
  gyr_t[1] = g.gyro.y;
  gyr_t[2] = g.gyro.z;
  portEXIT_CRITICAL_ISR(&timerMux);
  // Give a semaphore that we can check in the loop
  xSemaphoreGiveFromISR(timerSemaphore, NULL);
  // It is safe to use digitalRead/Write here if you want to toggle an output
  //digitalWrite(LED_PIN, !digitalRead(LED_PIN));
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
      float acc[3];
      float gyr[3];
      portENTER_CRITICAL(&timerMux);
      for(int i=0;i<3;i++)
      {
        acc[i] = acc_t[i];
        gyr[i] = gyr_t[i];
      }
      portEXIT_CRITICAL(&timerMux);
      
    }
}