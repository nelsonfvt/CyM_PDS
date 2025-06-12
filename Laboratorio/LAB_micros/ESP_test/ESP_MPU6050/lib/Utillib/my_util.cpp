#include "my_util.h"

//De bytes a float
float fromBytesToFloat(byte* packet)
{
  float f;
  memcpy(&f, packet, sizeof(f));
  return f;
}

void fromFloatToBytes(byte* bytes, float f)
{
  int length = sizeof(float);
  for(int i = 0; i<length; i++)
  {
    bytes[i] = ((byte*)&f)[i];
  }
}