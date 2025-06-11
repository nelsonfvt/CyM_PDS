#include "my_timer2.h"
#include "stm32f7xx.h"

void Configura_timer2()
{
	RCC->APB1ENR|=RCC_APB1ENR_TIM2EN;
	TIM2->CNT=0xFFFFFFFF;
	TIM2->CR1|=TIM_CR1_CEN;
	TIM2->ARR=31999;//31999;//16000;//31999;//16000;//63999;
	TIM2->PSC=0;//0;//41;//124;//41;//249;
}
