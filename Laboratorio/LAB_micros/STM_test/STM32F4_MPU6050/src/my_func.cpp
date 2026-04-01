#include "my_func.h"
#include <usart2.h>
#include <util.h>

void send_pack(char c_sens, float *data)
{
	char buffer[15];
	buffer[0] = c_sens;
	buffer[1] = c_sens;
	for(int i = 0;i<3;i++)
	{
		uint8_t bytes[4];
		fromFloatToBytes(bytes ,data[i]);

		for(int k = 0; k<4; k++)
			buffer[(i*4) + k+2] = bytes[k];

		
	}
	buffer[14] = '\n';

	writebuff_usart2(buffer,15);
}

void send_pack(char c_sens, float *data1, float *data2)
{
	char buffer[27];
	buffer[0] = c_sens;
	buffer[1] = c_sens;
	for(int i = 0;i<3;i++)
	{
		uint8_t bytes[4];
		fromFloatToBytes(bytes ,data1[i]);

		for(int k = 0; k<4; k++)
			buffer[(i*4) + k+2] = bytes[k];
		
	}

	for(int i = 3; i<6 ;i++)
	{
		uint8_t bytes[4];
		fromFloatToBytes(bytes ,data2[i-3]);

		for(int k = 0; k<4; k++)
			buffer[(i*4) + k+2] = bytes[k];
		
	}

	buffer[26] = '\n';

	writebuff_usart2(buffer,27);
}


