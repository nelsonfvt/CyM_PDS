#include "i2c1.h"

void Configura_i2c1()
{
    // Activa reloj y GPIO I2C1 
    RCC->APB1ENR |= RCC_APB1ENR_I2C1EN; //Activacion reloj i2c1
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOBEN; //Activa pueto B
    
    //Configurando pin B6
    GPIOB->MODER |= (2UL<<GPIO_MODER_MODER6_Pos); //Pin B6 modo alternativo
    GPIOB->AFR[0] |= (4UL<<GPIO_AFRL_AFSEL6_Pos); //Funcion alternativa 4 B6
    GPIOB->OTYPER |= GPIO_OTYPER_OT6; //Open-Drain B6
    GPIOB->OSPEEDR |= (2UL<<GPIO_OSPEEDR_OSPEED6_Pos); //High Speed
    GPIOB->PUPDR |= (1UL<<GPIO_PUPDR_PUPD6_Pos); //Pull-up activado B6
    //Configurando pin B7
    GPIOB->MODER |= (2UL<<GPIO_MODER_MODER7_Pos); //Pin B7 modo alternativo
    GPIOB->AFR[0] |= (4UL<<GPIO_AFRL_AFSEL7_Pos); //Funcion alternativa 4 B7
    GPIOB->OTYPER |= GPIO_OTYPER_OT7; //Open-Drain B7
    GPIOB->OSPEEDR |= (2UL<<GPIO_OSPEEDR_OSPEED7_Pos); //High Speed
    GPIOB->PUPDR |= (1UL<<GPIO_PUPDR_PUPD7_Pos); //Pull-up activado B7

    //Modulo I2C1
    I2C1->CR1 |= I2C_CR1_SWRST;//reset
    I2C1->CR1 &= ~I2C_CR1_SWRST;
    // Velocidad de transmision
    I2C1->CR2 |= 16;
    I2C1->CCR = 160/(2.0);
    I2C1->TRISE = 16+1;
    I2C1->CR1 |= I2C_CR1_PE; // habilta periferico
}

void Start_i2c1()
{
    I2C1->CR1 |= I2C_CR1_ACK; //habilita ACK
    I2C1->CR1 |= I2C_CR1_START; //
    while(!(I2C1->SR1 & I2C_SR1_SB)); //Espera bit SB
}

void Stop_i2c1()
{
    I2C1->CR1 |= I2C_CR1_STOP;  // Stop I2C
}

void Address_i2c1(uint8_t addr)
{
    I2C1->DR = addr;  //  send the address
	while (!(I2C1->SR1 & I2C_SR1_ADDR));  // wait for ADDR bit to set
	uint8_t temp = I2C1->SR1 | I2C1->SR2;  // read SR1 and SR2 to clear the ADDR bit
}

void SendByte_i2c1(uint8_t data)
{
    while (!(I2C1->SR1 & I2C_SR1_TXE));  // wait for TXE bit to set
	I2C1->DR = data;
	while (!(I2C1->SR1 & I2C_SR1_BTF));  // wait for BTF bit to set
}

void SendBuff_i2c1(uint8_t *data, uint8_t size)
{
    for(uint8_t i = 0; i<size; i++)
    {
        while (!(I2C1->SR1 & I2C_SR1_TXE));  // wait for TXE bit to set
        I2C1->DR = data[i];
    }
    while (!(I2C1->SR1 & I2C_SR1_BTF));  // wait for BTF bit to set
}

void ReadByte_i2c1(uint8_t addr, uint8_t *data)
{
    I2C1->DR = addr; //envia dirección esclava
    while(!(I2C1->SR1 & I2C_SR1_ADDR)); //espera envio addr

    I2C1->CR1 &= ~I2C_CR1_ACK;  // clear the ACK bit
    uint8_t temp = I2C1->SR1 | I2C1->SR2; // read SR1 and SR2 to clear the ADDR bit
    I2C1->CR1 |= I2C_CR1_STOP;  // Stop I2C

    while (!(I2C1->SR1 & I2C_SR1_RXNE));  // wait for RxNE to set

    *data = I2C1->DR; //lee el dato
}

void ReadBuff_i2c1(uint8_t addr, uint8_t *data, uint8_t size)
{
    uint8_t n_bytes = size;

    I2C1->DR = addr; //envia dirección esclava
    while(!(I2C1->SR1 & I2C_SR1_ADDR)); //espera envio addr

    uint8_t temp = I2C1->SR1 | I2C1->SR2;  // read SR1 and SR2 to clear the ADDR bit

    while(n_bytes>2)
    {
        while(!(I2C1->SR1 & I2C_SR1_RXNE));  // wait for RxNE to set

        data[size-n_bytes] = I2C1->DR;  // copy the data into the buffer

        I2C1->CR1 |= I2C_CR1_ACK;  // Set the ACK bit to Acknowledge the data received

        n_bytes--;
    }

    // leyendo penultimo
    while(!(I2C1->SR1 & I2C_SR1_RXNE));  // wait for RxNE to set
	data[size-n_bytes] = I2C1->DR;

    I2C1->CR1 &= ~I2C_CR1_ACK;  // clear the ACK bit 

    I2C1->CR1 |= I2C_CR1_STOP;  // Stop I2C

    n_bytes--;

    //leyendo ultimo
    while(!(I2C1->SR1 & I2C_SR1_RXNE));  // wait for RxNE to set
    data[size-n_bytes] = I2C1->DR;
}