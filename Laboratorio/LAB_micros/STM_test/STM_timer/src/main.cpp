#include "stm32f401xe.h"
#include <stdio.h>

int isrCounter = 0;
char buffer [50];

void send(char*, uint16_t);
void funcion_aux();

extern "C"{
void TIM2_IRQHandler(void)
{
    TIM2->SR &= (~TIM_SR_UIF);  //apaga bandera timer
    isrCounter += 1;
    
    funcion_aux();
        
    GPIOC->ODR ^= GPIO_ODR_OD13; //cambio LED
}
}

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

void Configura_timer2()
{
	RCC->APB1ENR|=RCC_APB1ENR_TIM2EN;
	TIM2->CNT=0xFFFFFFFF;
	TIM2->CR1|=TIM_CR1_CEN;
	TIM2->ARR=16000;//31999;//16000;//63999;
	TIM2->PSC=41;//124;//41;//249;
}

int main()
{
    //Activa pin 13 salida - LED
    RCC->AHB1ENR|=RCC_AHB1ENR_GPIOCEN;
	GPIOC->MODER|=(1UL<<GPIO_MODER_MODER13_Pos);
	GPIOC->ODR|=GPIO_ODR_OD13;

	// configuracion usart2
	Configura_usart2();

    //Configuracion timer 2
	Configura_timer2();
	//Habilita interrupcion timer2
	NVIC_EnableIRQ(TIM2_IRQn);
	TIM2->DIER|=TIM_DIER_UIE;

    while(1)
    {
        
    }
    return 0;
}

void send(char* buffer, uint16_t n)
{
    uint16_t count = 0;
    while(count < n)
    {
        while ((USART2->SR & 0x80) == 0); //esperar puerto habilitado
        USART2->DR = buffer[count];
        count ++;
    }
}

void funcion_aux()
{
    if(isrCounter > 99)
    {
        isrCounter = 0;
        int n = sprintf(buffer, "*****Reinicia*****\n");
        send(buffer, n);
    }
    //print("Counter = ", 10);
    int n = sprintf(buffer, "Contador = %d\n",isrCounter);
    send(buffer,n);
}