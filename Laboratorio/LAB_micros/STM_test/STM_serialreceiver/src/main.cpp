#include "stm32f401xe.h"
#include <cstring>

void Configura_usart2(void)
{
	RCC->AHB1ENR|= RCC_AHB1ENR_GPIOAEN;
	GPIOA->MODER|= (2UL<<GPIO_MODER_MODER2_Pos);
	GPIOA->MODER|= (2UL<<GPIO_MODER_MODER3_Pos);
	GPIOA->AFR[0]|= (7UL<<GPIO_AFRL_AFSEL2_Pos);
	GPIOA->AFR[0]|= (7UL<<GPIO_AFRL_AFSEL3_Pos);
	RCC->APB1ENR|=RCC_APB1ENR_USART2EN;
	USART2->BRR=(unsigned int)(16000000/115200);
	USART2->CR1|=(USART_CR1_RE|USART_CR1_TE);
	USART2->CR2=0;
	USART2->CR3=0;
	USART2->CR1|=USART_CR1_UE;
}

/*Funciones de conversion - definiciones*/
float fromBytesToFloat(uint8_t*);
void fromFloatToBytes(uint8_t* , float);

uint32_t readBytesUntil(char, char*, uint32_t);
void writebuffer(char*, uint32_t);
void find_sep(uint8_t*, uint8_t*, char*);

int main()
{
    //Variables
    char myData[10] = {0};
    char sendData[9];
    uint8_t s1[4];
    uint8_t s2[4];

    float f1;
    float f2;
    
    // configuracion usart2
	Configura_usart2();

    //Activa pin 13 salida - LED
    RCC->AHB1ENR|=RCC_AHB1ENR_GPIOCEN;
	GPIOC->MODER|=(1UL<<GPIO_MODER_MODER13_Pos);
	GPIOC->ODR|=GPIO_ODR_OD13;

    while(1)
	{
        GPIOC->ODR ^= GPIO_ODR_OD13; //cambio LED
        uint32_t m = readBytesUntil('\n', myData, 30);
        //extrayendo partes
        find_sep(s1, s2, myData);

        //operaciones
        f1 = fromBytesToFloat(s1);
        f1 = f1 * 0.45;

        f2 = fromBytesToFloat(s2);
        f2 = f2 * 0.55;

        // bytes para enviar
        fromFloatToBytes(s1, f1);
        fromFloatToBytes(s2, f2);

        // Al buffer de datos de envio
        sendData[0] =s1[0];
        sendData[1] =s1[1];
        sendData[2] =s1[2];
        sendData[3] =s1[3];
        sendData[4] =s2[0];
        sendData[5] =s2[1];
        sendData[6] =s2[2];
        sendData[7] =s2[3];
        sendData[8] = '\n';

        writebuffer(sendData, 9);
    }
    return 0;
}

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

uint32_t readBytesUntil(char term, char* buffer, uint32_t max_c)
{
    uint32_t count = 0;
    char byte = term + 1;
    
    while( count < max_c && byte != term)
    {
        if(USART2->SR & USART_SR_RXNE)
        {
            byte = USART2->DR;
            if(byte != term)
                buffer[count] = byte;
            count++;
        }
    }
    
    return count;
}

void writebuffer(char* buffer, uint32_t n)
{
    uint32_t count = 0;
    while(count < n)
    {
        while ((USART2->SR & 0x80) == 0);//esperar puerto habilitado
        USART2->DR = buffer[count];
        count++;
		
    }
}

void find_sep(uint8_t* buf1, uint8_t* buf2, char* cad)
{
    for(int i; i<4; i++)
    {
        buf1[i] = (uint8_t)cad[i];
        buf2[i] = (uint8_t)cad[i+5];
    }
}