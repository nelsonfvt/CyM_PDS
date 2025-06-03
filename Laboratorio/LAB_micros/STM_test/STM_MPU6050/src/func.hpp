#ifndef FUNC_HPP
#define FUNC_HPP

#include "stm32f401xe.h"

void Configura_timer2();
void Configura_usart2();
void Configura_i2c1();
void MstTx_i2c1(uint16_t, uint16_t, uint8_t);
void MstRx_i2c1(uint8_t, uint8_t, uint8_t*);

#endif