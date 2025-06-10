#include "util.h"
#include <cstring>

/*Funciones de conversion - declaraciones*/
float fromBytesToFloat(uint8_t* packet)
{
    float f;
    memcpy(&f, packet, sizeof(f));
    return f;
}

void fromFloatToBytes(uint8_t* bytes, float f)
{
    int length = sizeof(float);
    for(int i = 0; i<length; i++)
    {
        bytes[i] = ((uint8_t*)&f)[i];
    }
}