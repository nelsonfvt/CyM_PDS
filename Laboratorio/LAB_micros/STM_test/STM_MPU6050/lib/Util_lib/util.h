#ifndef UTIL_H
#define UTIL_H

#include "stm32f401xe.h"

/*Funciones de conversion - definiciones*/
float fromBytesToFloat(uint8_t*);
void fromFloatToBytes(uint8_t* , float);


#endif