#ifndef I2C1_H
#define I2C1_H

#include "stm32f401xe.h"

void Configura_i2c1();
void Start_i2c1();
void Stop_i2c1();

void Address_i2c1(uint8_t);
void SendByte_i2c1(uint8_t);
void SendBuff_i2c1(uint8_t *, uint8_t);

void ReadByte_i2c1(uint8_t, uint8_t *);
void ReadBuff_i2c1(uint8_t, uint8_t *, uint8_t);


#endif