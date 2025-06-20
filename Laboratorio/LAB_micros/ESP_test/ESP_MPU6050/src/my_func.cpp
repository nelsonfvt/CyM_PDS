#include "my_func.h"
#include <Arduino.h>
#include <my_util.h>

void en_pack(char c_sens,char* buffer, float *data)
{
	buffer[0] = c_sens;
	for(int i = 0;i<3;i++)
	{
		byte ltes[4];
		fromFloatToBytes(ltes ,data[i]);

		for(int k = 0; k<4; k++)
			buffer[(i*4) + k+1] = ltes[k];

		
	}
	buffer[13] = '\n';
}

void en_pack(char c_sens, char *buffer, float *data1, float *data2)
{
	buffer[0] = c_sens;
	for(int i = 0;i<3;i++)
	{
		byte ltes[4];
		fromFloatToBytes(ltes ,data1[i]);

		for(int k = 0; k<4; k++)
			buffer[(i*4) + k+1] = ltes[k];
		
	}

	for(int i = 3; i<6 ;i++)
	{
		byte ltes[4];
		fromFloatToBytes(ltes ,data2[i-3]);

		for(int k = 0; k<4; k++)
			buffer[(i*4) + k+1] = ltes[k];
		
	}

	buffer[25] = '\n';
}