#ifndef MY_USART3_H
#define MY_USART3_H

#include "stm32f7xx.h"

void Configura_usart3();

void writebuff_usart3(char*, uint16_t);
uint32_t readUntil_usart3(char, char*, uint32_t);

#endif