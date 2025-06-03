#include "func.hpp"

void Configura_timer2()
{
	RCC->APB1ENR|=RCC_APB1ENR_TIM2EN;
	TIM2->CNT=0xFFFFFFFF;
	TIM2->CR1|=TIM_CR1_CEN;
	TIM2->ARR=16000;//31999;//16000;//63999;
	TIM2->PSC=41;//124;//41;//249;
}

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

void Configura_i2c1()
{
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOBEN; //Activa pueto B
    //Configurando pin B6
    GPIOB->MODER |= (2UL<<GPIO_MODER_MODER6_Pos); //Pin B6 modo alternativo
    GPIOB->AFR[0] |= (4UL<<GPIO_AFRL_AFSEL6_Pos); //Funcion alternativa 4 B6
    GPIOB->OTYPER |= GPIO_OTYPER_OT6; //Open-Drain B6
    GPIOB->PUPDR |= (1UL<<GPIO_PUPDR_PUPD6_Pos); //Pull-up activado B6
    //Configurando pin B7
    GPIOB->MODER |= (2UL<<GPIO_MODER_MODER7_Pos); //Pin B7 modo alternativo
    GPIOB->AFR[0] |= (4UL<<GPIO_AFRL_AFSEL7_Pos); //Funcion alternativa 4 B7
    GPIOB->OTYPER |= GPIO_OTYPER_OT7; //Open-Drain B7
    GPIOB->PUPDR |= (1UL<<GPIO_PUPDR_PUPD7_Pos); //Pull-up activado B7

    //Activacion reloj i2c1
    RCC->APB1ENR |= RCC_APB1ENR_I2C1EN;

    //Modulo I2C1
    I2C1->CR1 |= I2C_CR1_SWRST;//reset
    I2C1->CR1 &= ~I2C_CR1_SWRST;
    // Velocidad de transmision
    I2C1->CR2 |= 16;
    I2C1->CCR = 160/(2.0);
    I2C1->TRISE = 16+1;
    I2C1->CR1 |= I2C_CR1_PE; // habilta peroferico
}

void MstTx_i2c1(uint16_t slv_addr, uint16_t reg_addr, uint8_t data)
{


}

void MstRx_i2c1(uint8_t slv_addr, uint8_t reg_addr, uint8_t* data)
{
    uint16_t tmp = 0x00;
    I2C1->CR1 |= I2C_CR1_START; // Master mode - inicio
    while(!(I2C1->SR1 & I2C_SR1_SB)); // Espera
    tmp = I2C1->SR1; //limpia
    I2C1->DR = slv_addr; //carga slave address
    while(!(I2C1->SR1 & I2C_SR1_ADDR)); //espera envio direccion
    tmp = I2C1->SR1; // limpia
    tmp = I2C1->SR2; //limpia
    while(!(I2C1->SR1 & I2C_SR1_TXE)); //espera linea libre
    I2C1->DR = reg_addr; // carga segunda direccion
    while(!(I2C1->SR1 & I2C_SR1_ADDR)); //espera envio direccion
    tmp = I2C1->SR1; // limpia
    tmp = I2C1->SR2; //limpia
}