#ifndef MYMPU6050_H
#define MYMPU6050_H

#include "stm32f7xx.h"

void MPU_write(uint8_t, uint8_t, uint8_t);
void MPU_read(uint8_t, uint8_t, uint8_t *);

void MPU_init();
void MPU6050_Read_Accel (float *);
void MPU6050_Read_Gyro (float *);

#endif