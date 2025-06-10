#include "my_func.h"
#include <my_usart3.h>
#include <util.h>

void send_pack(char c_sens, float *data)
{
	char buffer[14];
	buffer[0] = c_sens;
	for(int i = 0;i<3;i++)
	{
		uint8_t bytes[4];
		fromFloatToBytes(bytes ,data[i]);

		for(int k = 0; k<4; k++)
			buffer[(i*4) + k+1] = bytes[k];

		
	}
	buffer[13] = '\n';

	writebuff_usart3(buffer,14);
}

void send_pack(char c_sens, float *data1, float *data2)
{
	char buffer[26];
	buffer[0] = c_sens;
	for(int i = 0;i<3;i++)
	{
		uint8_t bytes[4];
		fromFloatToBytes(bytes ,data1[i]);

		for(int k = 0; k<4; k++)
			buffer[(i*4) + k+1] = bytes[k];
		
	}

	for(int i = 3; i<6 ;i++)
	{
		uint8_t bytes[4];
		fromFloatToBytes(bytes ,data2[i-3]);

		for(int k = 0; k<4; k++)
			buffer[(i*4) + k+1] = bytes[k];
		
	}

	buffer[25] = '\n';

	writebuff_usart3(buffer,26);
}


