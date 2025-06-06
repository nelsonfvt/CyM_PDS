#ifndef USART2_H
#define USART2_H

#include "stm32f401xe.h"

void Configura_usart2();

void writebuff_usart2(char*, uint16_t);
uint32_t readUntil_usart2(char, char*, uint32_t);

#endif