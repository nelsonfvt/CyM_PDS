#ifndef MYMPU6050_H
#define MYMPU6050_H

#include <Wire.h>

void MPU_write(char, char, char);
void MPU_read(char, char, char *);

void MPU_init();
void MPU6050_Read_Accel (float *);
void MPU6050_Read_Gyro (float *);

#endif