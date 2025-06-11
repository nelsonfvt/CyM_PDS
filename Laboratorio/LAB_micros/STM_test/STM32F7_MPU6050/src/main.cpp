#include "stm32f767xx.h"
#include <my_timer2.h>
#include <my_usart3.h>
#include <MyMPU6050.h>
#include "my_func.h"

float Acc[3];
float Gyr[3];

extern "C"{
    void TIM2_IRQHandler(void)
    {
        TIM2->SR &= (~TIM_SR_UIF);  //apaga bandera timer
        
        MPU6050_Read_Accel(Acc);
        MPU6050_Read_Gyro(Gyr);
        send_pack('a', Acc, Gyr);

        // uint8_t check;
        // MPU_read(0xD0, 0x75, &check);
        // char ele = (char)check;
        // writebuff_usart3(&ele, 1);


        GPIOB->ODR ^= GPIO_ODR_OD0;
        GPIOB->ODR ^= GPIO_ODR_OD7;
        GPIOB->ODR ^= GPIO_ODR_OD14;
    }
}

int main()
{
    // Turn on the GPIOB peripheral
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOBEN;

    // Put the pin in general purpose output mode
    GPIOB->MODER |= GPIO_MODER_MODER0_0;
    GPIOB->MODER |= GPIO_MODER_MODER7_0;
    GPIOB->MODER |= GPIO_MODER_MODER14_0;
    // Turn off leds
    GPIOB->BSRR = GPIO_BSRR_BR_0; //verde
    GPIOB->BSRR = GPIO_BSRR_BR_7; //azul
    GPIOB->BSRR = GPIO_BSRR_BR_14; //rojo

    //Configurando USART2
    Configura_usart3();

    // Inicializa MPU
    MPU_init();
    

    Configura_timer2();
    //Habilita interrupcion timer2
	NVIC_EnableIRQ(TIM2_IRQn);
	TIM2->DIER|=TIM_DIER_UIE;

    while(1)
    {
       
    }
    return 0;
}