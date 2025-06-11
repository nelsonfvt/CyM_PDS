#include "my_i2c.h"
#include <my_usart3.h>

void Configura_i2c1()
{
    // Activa reloj y GPIO I2C1 
    RCC->APB1ENR |= RCC_APB1ENR_I2C1EN; //Activacion reloj i2c1
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOBEN; //Activa pueto B
    
    //Configurando pin B8 SCL
    GPIOB->MODER |= (2UL<<GPIO_MODER_MODER8_Pos); //Pin B6 modo alternativo
    GPIOB->AFR[1] |= (4UL<<GPIO_AFRH_AFRH1_Pos); //Funcion alternativa 4 B6
    GPIOB->OTYPER |= GPIO_OTYPER_OT8; //Open-Drain B6
    GPIOB->OSPEEDR |= (2UL<<GPIO_OSPEEDR_OSPEEDR8_Pos); //High Speed
    GPIOB->PUPDR |= (1UL<<GPIO_PUPDR_PUPDR8_Pos); //Pull-up activado B6
    //Configurando pin B9 SDA
    GPIOB->MODER |= (2UL<<GPIO_MODER_MODER9_Pos); //Pin B7 modo alternativo
    GPIOB->AFR[1] |= (4UL<<GPIO_AFRH_AFRH2_Pos); //Funcion alternativa 4 B7
    GPIOB->OTYPER |= GPIO_OTYPER_OT9; //Open-Drain B7
    GPIOB->OSPEEDR |= (2UL<<GPIO_OSPEEDR_OSPEEDR9_Pos); //High Speed
    GPIOB->PUPDR |= (1UL<<GPIO_PUPDR_PUPDR9_Pos); //Pull-up activado B7

    // Velocidad de transmision
    RCC->DCKCFGR2 |= 0x80000; //??
    I2C1->TIMINGR |= (6UL<<I2C_TIMINGR_PRESC_Pos);
    I2C1->TIMINGR |= 9UL; //SCLL
    I2C1->TIMINGR |= (9UL<<I2C_TIMINGR_SCLH_Pos); //SCLH
    //I2C1->CR1 |= I2C_CR1_TXIE; //???

    I2C1->CR1 |= I2C_CR1_PE; // habilta periferico 
}

void SendByte_i2c1(uint8_t s_addr, char data)
{
    //Master_initializer(s_addr, 1, 1);
    I2C1->CR2 &= ~I2C_CR2_ADD10; // 7 bits
    I2C1->CR2 |= ((1UL<<I2C_CR2_NBYTES_Pos) | s_addr);//0x020120D0; //CR2 PARA TRANSFERIR BYTE 
    I2C1->CR2 &= ~I2C_CR2_RD_WRN; // escribir
    I2C1->CR2 |= I2C_CR2_START;
    //while(!(I2C1->ISR & I2C_ISR_NACKF));
    while(!(I2C1->ISR & I2C_ISR_TXE)); // TXIS espera envio s_addr
    char check = 'Z';
    writebuff_usart3(&check, 1);
    
    I2C1->TXDR = data;
    
    while(!(I2C1->ISR & I2C_ISR_TXE)); //espera envio data
    
    while(!(I2C1->ISR & I2C_ISR_STOPF)); //envio stop
    I2C1->ISR &= ~I2C_ISR_STOPF; //borra bandera STOP
    I2C1->CR2 = 0;
}

void SendBuff_i2c1(uint8_t s_addr, uint8_t r_addr, char *data, uint8_t size)
{
    
	//Master_init_i2c1(s_addr, size, 1); // size + 1??

    I2C1->TXDR  = r_addr; //carga dirección registro esclavo
    I2C1->CR2 |= I2C_CR2_START; // genera start para transmitir registro esclavo
    while(!(I2C1->ISR & I2C_ISR_TXE)); // espera TX de r_addr

    uint8_t r_cont = size;
    while(r_cont > 0)
    {
        I2C1->TXDR = data[size-r_cont];
        while(!(I2C1->ISR & I2C_ISR_TXIS)); // espera TX de data
        r_cont--;
    }

    //while(!(I2C1->ISR & I2C_ISR_TC)); //transmision completada
    I2C1->CR2 = 0;
}

void ReadByte_i2c1(uint8_t s_addr, char *data)
{
    I2C1->CR2 = 0x020124D0; //CR2 para recibir
    while(!(I2C1->ISR & I2C_ISR_RXNE)); // espera recepción
    data[0] = I2C1->RXDR;
    while(!(I2C1->ISR & I2C_ISR_STOPF)); // espera stop
    I2C1->CR2 = 0; // reset CR2
}

void ReadBuff_i2c1(uint8_t s_addr, uint8_t r_addr, char *data, uint8_t size)
{
    //Master_init_i2c1(s_addr, size+1, 0); // size + 1??

    I2C1->TXDR = r_addr; //carga dirección registro esclavo
    I2C1->CR2 |= I2C_CR2_START; // genera start para transmitir registro esclavo
    while(!(I2C1->ISR & I2C_ISR_TXE));

    char check = 'X';
    writebuff_usart3(&check, 1);


    uint8_t r_cont = size;
    while(r_cont > 0)
    {
        while(!(I2C1->ISR & I2C_ISR_RXNE));
        data[size-r_cont] = I2C1->RXDR;
        r_cont--;
    }
    I2C1->CR2 = 0;
}

void Configura_i2c2()
{
    // Activa reloj y GPIO I2C1 
    RCC->APB1ENR |= RCC_APB1ENR_I2C2EN; //Activacion reloj i2c2
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOFEN; //Activa pueto F
    
    //Configurando pin F1 SCL
    GPIOF->MODER |= (2UL<<GPIO_MODER_MODER1_Pos); //Pin F1 modo alternativo
    GPIOF->AFR[0] |= (4UL<<GPIO_AFRL_AFRL1_Pos); //Funcion alternativa 4 B6
    GPIOF->OTYPER |= GPIO_OTYPER_OT1; //Open-Drain B6
    GPIOF->OSPEEDR |= (2UL<<GPIO_OSPEEDR_OSPEEDR1_Pos); //High Speed
    GPIOF->PUPDR |= (1UL<<GPIO_PUPDR_PUPDR1_Pos); //Pull-up activado B6
    //Configurando pin F0 SDA
    GPIOF->MODER |= (2UL<<GPIO_MODER_MODER0_Pos); //Pin B7 modo alternativo
    GPIOF->AFR[0] |= (4UL<<GPIO_AFRL_AFRL0_Pos); //Funcion alternativa 4 B7
    GPIOF->OTYPER |= GPIO_OTYPER_OT0; //Open-Drain B7
    GPIOF->OSPEEDR |= (2UL<<GPIO_OSPEEDR_OSPEEDR0_Pos); //High Speed
    GPIOF->PUPDR |= (1UL<<GPIO_PUPDR_PUPDR0_Pos); //Pull-up activado B7

    // Velocidad de transmision
    RCC->DCKCFGR2 |= 0x80000; //??
    I2C2->TIMINGR = 0x00303D5B;
    
    I2C2->CR1 |= I2C_CR1_ANFOFF; //filtro de ruido desactivado
    I2C2->CR1 |= I2C_CR1_NOSTRETCH; //nostretch desactivado

    I2C2->CR1 |= I2C_CR1_PE; // habilta periferico 
}

void Reset_i2c2()
{
    I2C2->CR1 &= ~I2C_CR1_PE;
	while (I2C2->CR1 & I2C_CR1_PE);
	I2C2->CR1 |=I2C_CR1_PE;
}

void SendByte_i2c2(uint8_t s_addr, uint8_t data)
{
    //Master_initializer
    I2C2->CR2 &= ~I2C_CR2_ADD10; // 7 bits
    I2C2->CR2 |= I2C_CR2_AUTOEND; //Auto
    I2C2->CR2 |= ((1UL<<I2C_CR2_NBYTES_Pos) | s_addr);//0x020120D0; //CR2 PARA TRANSFERIR BYTE 
    I2C2->CR2 &= ~I2C_CR2_RD_WRN; // escribir
    I2C2->CR2 |= I2C_CR2_START;
    while(!(I2C2->ISR & I2C_ISR_TXIS));// TXIS espera envio s_addr
    
    int cont = 0;
    while(cont<1)
    {
        if(I2C2->ISR & I2C_ISR_TXE) // buffer disponible
        {
            I2C2->TXDR = data; // carga dato
            cont++;
        }
    }
    while(!(I2C2->ISR & I2C_ISR_STOPF)); //espera STOP
    I2C2->CR2 = 0;
}

void SendBuff_i2c2(uint8_t s_addr, uint8_t* data, uint8_t size)
{
    I2C2->CR2 &= ~I2C_CR2_ADD10; // 7 bits
    I2C2->CR2 |= I2C_CR2_AUTOEND; //Auto
    I2C2->CR2 |= ((size<<I2C_CR2_NBYTES_Pos) | s_addr);//0x020120D0; //CR2 PARA TRANSFERIR BYTE 
    I2C2->CR2 &= ~I2C_CR2_RD_WRN; // escribir
    I2C2->CR2 |= I2C_CR2_START;
    while(!(I2C2->ISR & I2C_ISR_TXIS));// TXIS espera envio s_addr

    uint8_t cont = 0;
    while(cont<size) //Espera envio comleto 1 Byte
    {
        if(I2C2->ISR & I2C_ISR_TXE) // buffer disponible
        {
            I2C2->TXDR = data[cont]; // carga dato
            cont++;
        }
    }
    while(!(I2C2->ISR & I2C_ISR_STOPF)); //espera STOP
}

void ReadByte_i2c2(uint8_t s_addr, uint8_t *data)
{
    I2C2->CR2 &= ~I2C_CR2_ADD10; // 7 bits
    I2C2->CR2 |= I2C_CR2_AUTOEND;
    I2C2->CR2 |= ((1UL<<I2C_CR2_NBYTES_Pos) | (s_addr | 0x01)); //CR2 Para recibir //I2C2->CR2 = 0x020124D0;
    I2C2->CR2 |= I2C_CR2_RD_WRN; // leer
    I2C2->CR2 |= I2C_CR2_START;
    
    while(!(I2C2->ISR & I2C_ISR_STOPF))//espera hasta que se genera stop
    {
        if(I2C2->ISR & I2C_ISR_RXNE) // buferr disponible
        {
            data[0] = I2C2->RXDR;
        }
    }

    I2C2->CR2 = 0; // reset CR2    
}

void ReadBuff_i2c2(uint8_t s_addr, uint8_t *data, uint8_t size)
{
    I2C2->CR2 &= ~I2C_CR2_ADD10; // 7 bits
    I2C2->CR2 |= I2C_CR2_AUTOEND;
    I2C2->CR2 |= ((1UL<<I2C_CR2_NBYTES_Pos) | (s_addr | 0x01)); //CR2 Para recibir //I2C2->CR2 = 0x020124D0;
    I2C2->CR2 |= I2C_CR2_RD_WRN; // leer
    I2C2->CR2 |= I2C_CR2_START;

    uint8_t cont = 0;
    while(!(I2C2->ISR & I2C_ISR_STOPF))//espera hasta que se genera stop
    {
        if(I2C2->ISR & I2C_ISR_RXNE) // buferr disponible
        {
            data[cont] = I2C2->RXDR;
            cont++;
        }
    }

    I2C2->CR2 = 0; // reset CR2
}