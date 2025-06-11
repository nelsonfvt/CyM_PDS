#ifndef MY_I2C_H
#define MY_I2C_H

#include "stm32f767xx.h"

//i2c1
void Configura_i2c1();

void SendByte_i2c1(uint8_t, char);
void SendBuff_i2c1(uint8_t , uint8_t, char *, uint8_t);

void ReadByte_i2c1(uint8_t , char *);
void ReadBuff_i2c1(uint8_t , uint8_t, char *, uint8_t);

//i2c2
void Configura_i2c2();

void Reset_i2c2();

void SendByte_i2c2(uint8_t, uint8_t);
void SendBuff_i2c2(uint8_t, uint8_t *, uint8_t);
void ReadByte_i2c2(uint8_t, uint8_t *);
void ReadBuff_i2c2(uint8_t, uint8_t *, uint8_t);

#endif