#include "usart2.h"


void Configura_usart2()
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

void writebuff_usart2(char* buffer, uint16_t n)
{
    uint16_t count = 0;
    while(count < n)
    {
        while ((USART2->SR & 0x80) == 0); //esperar puerto habilitado
        USART2->DR = buffer[count];
        count ++;
    }
}

uint32_t readUntil_usart2(char term, char* buffer, uint32_t max_c)
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