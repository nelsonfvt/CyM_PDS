#include "stm32f401xe.h"
#include "my_func.h"
#include <MyMPU6050.h>
#include <i2c1.h>
#include <util.h>
#include <usart2.h>
#include <my_timer2.h>
#include <stdio.h>

float Acc[3];
float Gyr[3];

extern "C"{
void TIM2_IRQHandler(void)
{
    TIM2->SR &= (~TIM_SR_UIF);  //apaga bandera timer

    MPU6050_Read_Accel(Acc);
    MPU6050_Read_Gyro(Gyr);

    send_pack('a', Acc, Gyr);
    
    GPIOC->ODR ^= GPIO_ODR_OD13; //cambio LED
    
}
}

int main(){

    //Activa pin 13 salida - LED
    RCC->AHB1ENR|=RCC_AHB1ENR_GPIOCEN;
	GPIOC->MODER|=(1UL<<GPIO_MODER_MODER13_Pos);
	GPIOC->ODR|=GPIO_ODR_OD13;

    // configuracion usart2
	Configura_usart2();

	// configura i2c1
	Configura_i2c1();

    MPU_init();

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