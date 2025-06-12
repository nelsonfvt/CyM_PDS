#ifndef MY_UTIL_H
#define MY_UTIL_H

#include <Arduino.h>

void fromFloatToBytes(byte* , float);
float fromBytesToFloat(byte*);

#endif