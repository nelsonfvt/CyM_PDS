#include "my_usart3.h"


void Configura_usart3()
{
    RCC->AHB1ENR|= RCC_AHB1ENR_GPIODEN;
	GPIOD->MODER|= GPIO_MODER_MODER8_1;//(2UL<<GPIO_MODER_MODER8_Pos);
	GPIOD->MODER|= GPIO_MODER_MODER9_1;//(2UL<<GPIO_MODER_MODER9_Pos);
	GPIOD->AFR[1]|= (7UL<<0);
	GPIOD->AFR[0]|= (7UL<<4);
	RCC->APB1ENR|=RCC_APB1ENR_USART3EN;
	USART3->BRR=(unsigned int)(16000000/115200);
	USART3->CR1|=(USART_CR1_RE|USART_CR1_TE);
	USART3->CR2=0;
	USART3->CR3=0;
	USART3->CR1|=USART_CR1_UE;
}

void writebuff_usart3(char* buffer, uint16_t n)
{
    uint16_t count = 0;
    while(count < n)
    {
        while ((USART3->ISR & 0x80) == 0); //esperar puerto habilitado
        USART3->TDR = buffer[count];
        count ++;
    }
}

uint32_t readUntil_usart3(char term, char* buffer, uint32_t max_c)
{
    uint32_t count = 0;
    char byte = term + 1;
    
    while( count < max_c && byte != term)
    {
        if(USART3->ISR & USART_ISR_RXNE)
        {
            byte = USART3->RDR;
            if(byte != term)
                buffer[count] = byte;
            count++;
        }
    }
    
    return count;
}