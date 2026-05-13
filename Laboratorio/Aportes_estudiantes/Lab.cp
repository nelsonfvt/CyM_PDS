////////////////////////////////////////////
//            1. Catalina González        //
//            2. Juan Diego Vargas        //
//            3. Sebastian Niño           //
////////////////////////////////////////////
#include <stdio.h>
#include "stm32f7xx.h"
#include <string.h>
#include <math.h>
#include <stdlib.h>
//#include "stm32f7xx_hal.h"
//#include "nokia5110_LCD.h"
 
char numeros[10]={0x30,0x31,0x32,0x33,0x34,0x35,0x36,0x37,0x38,0x39};//VECTOR DE NUMEROS DEL 0-9 PARA RECONOCIMIENTO DE LCD
char posx[5]={'X',':','0','.','0'};
char posy[5]={'Y',':','0','.','0'};
char posz[5]={'Z',':','0','.','0'};
char dat[]={0,0,0}; //VECTOR PARA ALMECENARMIENTO DE 3 DATOS (EJER X,Y y Z)
char da1;           //VARIABLE PARA TRANSMITIR  EL VALOR DETECTADO POR EL SENSOR 
char POSX[2]={}, POSY[2]={},POSZ[2]={};//VECTORES DE 2 POSICIONES PARA CADA EJE
short Nx,Nx1,Nx2,Ny,Ny1,Ny2,Nz,Nz1,Nz2, numero, auxiliar,n; //VARIABLES TIPO SHORT PARA CONVERTIR LOS VALORES MEDIDOS

int x1=0,y1=0; //VARIABLES TIPO ENTERO PARA GUARDAR LOS VALORES COMVERTIDOS 
int t1,t2,t3,t4,t5,t6,cont=0,su=0; // VARIABLES USADAS
int a=0,b=0,c=0,d=0,e=0,f=0,g=0,h=0; // VARIABLES USADAS

static void SystemClock_Config(void);
void SystemIn(void);
//void ConfigSerial(void);
long double CTX, CTY, CTZ;
int Status2, Status4, Dato;
long i=0;
int Reg;
int8_t X1,X2,Y1,Y2,Z1,Z2;
uint8_t b2;
short TX,TY,TZ; //TOTAL X, TOTAL Y, TOTAL Z
uint16_t XS, YS, ZS;
char data;
char clear=0x01; // Limpiar panatlla
char mode =0x06; // CORRIMIENTO A LA DERECHA 
char disp_on = 0x0E;//Colocamos D2 que se encienda la pantalla, en D1 SI QUIERE PRENDER O APAGAR EL CURSOR Y D0 SI TITILA O NO TITILA
char set= 0x38; // COLOCAMOS EL DL EN D3 PARA TRABAJAR CON 8 BITS, D2 SE COLOCA N PARA TRABAJAR CON CIERTAS LINEAS Y F EN D1 PARA 5X7 CADA NUMERO
char ddramlL= 0x80; // MEMORIA PARA GUARDAR CARACTERES ESPECIALES PARA QUE SEAN MOSTRADOS EN LA 1 LINEA
char ddram2L= 0xC0; // MEMORIA PARA GUARDAR CARACTERES ESPECIAL PARA QUE SEAN MOSTRADOS EN LA 2 LINEA

void send_comando(char a){ // FUNCION PARA ESCRITURA  RS EN 0 Y RW 
	GPIOE -> ODR &=0xFF00; // LIMPIAR REGISTRO DE SALIDA DEL PUERTO E
	GPIOE -> ODR |=a;
	GPIOE -> ODR &=~(1UL<<8);//RS EN CERO
	GPIOE -> ODR |=(1UL<<9);//ENABLE EN 1
	for(int cont=0; cont <100000;cont++);
	GPIOE -> ODR &=~(1UL<<9);
}
void send_dato(char b){ // FUNCION PARA LEER 
	GPIOE -> ODR &=0xFF00;
	GPIOE -> ODR |=b;
	GPIOE -> ODR |=(1UL<<8);//RS EN CERO
	GPIOE -> ODR |=(1UL<<9);//ENABLE EN 1
	for(int cont=0; cont <100000;cont++);
	GPIOE -> ODR &=~(1UL<<9);
}
 
void I2C2_Init (void)   {
		RCC->AHB1ENR  |=  0x00000020; // Encender reloj puertoF PARA EL I2C2
		GPIOF->AFR[0] |=  0x00000044; // seleccion de la funcion alterna 4 del puerto F(I2C) para  PF1-SCL,PF0-SDA -> I2C2
		GPIOF->MODER  |=  0x0000000A; // PF0,PF1 => en modo alterno
		GPIOF->OTYPER |=  0x0003;     // Open drain  
    GPIOF->PUPDR |=  0x5;         // RESISTENCIA EN PULL UP PARA F0 Y F1
    GPIOF->OSPEEDR   |=  0xC;
     
    RCC->APB1ENR  |= 0x00400000;       // CLOCK (RELOJ) I2C2 DE 22BITS
    RCC->DCKCFGR2  |= 0x80000;         //Reloj de frecuencia del I2C2
     
    // SE DESHABILITA EL I2C2
    I2C2->CR1 &= ~I2C_CR1_PE; //deshabilita SCL y SDA para el periferico 
    while (I2C2->CR1 & I2C_CR1_PE);// SE COMPRUEBA QUE SE HAYA DESHABILITADO
    I2C2->TIMINGR |= 0x30420F13;         //TIMING DE 100KHZ			
    // DE 7 BITS
    I2C2->CR2 &=~ I2C_CR2_ADD10; //Modo maestro receptor, solo recibe 7 de 10 bits de comunicación
    I2C2->CR2 |= I2C_CR2_AUTOEND; //autofinalización activada
    I2C2->CR1 |= I2C_CR1_ANFOFF; //filtro de ruido desactivado
    I2C2->CR1 |= I2C_CR1_NOSTRETCH; //nostretch desactivado
    I2C2->CR1 |= I2C_CR1_PE; //habilita SCL y SDA para el periferico 
}

//FUNCION PARA ENVIAR 

void I2C2_Write (char Adr, char Dat){
    I2C2->CR2 |= 0x020220D0;	// CR2 COMFIGURADO EN MODO RECEPCION CON ADD10, DE 1 BYTE, Y LA DIRECCION QUE TENDRA EL SENSRO D0
    while (!(I2C2->ISR & I2C_ISR_TXIS)); // SE COMPRUEBA QUE SE HABILITE EL CR2
    I2C2->TXDR = Adr; // SE REALIZA LA TRANSMISION 
    while (!(I2C2->ISR & I2C_ISR_TXIS));// SE ESPERA QUE REALICE LA TRANSMISION 
    I2C2->TXDR = Dat; // SE REALIZA LA TRANSMISION 
    while (!(I2C2->ISR & I2C_ISR_TXE)); //SE ESPERA QUE SE REALICE 
    while (!(I2C2->ISR & I2C_ISR_STOPF));// SE DA EL BIT DE PARADA
    I2C2->ISR &= ~I2C_ISR_STOPF;    //PARA
}
 
//FUNCION PARA RECIBIR
int8_t I2C2_Read (char Adr){   
    I2C2->CR2 |= 0x020120D0; //SE ACTIVA EL CR2 PARA LA RECEPCION DE DATOS 
    while (!(I2C2->ISR & I2C_ISR_TXIS)); // SE DA UNA ESPERA PARA LA ACTIVACION 
    I2C2->TXDR = Adr; // SE RECIBE EL DATO ENVIADO POR EL SENSOR 
    while (!(I2C2->ISR & I2C_ISR_TXE)); // SE DA UNA VALIDACION DEL DATO REXIBIDO 
    while (!(I2C2->ISR & I2C_ISR_STOPF));// SE DA EL BOT DE PARADA
    I2C2->ISR &= ~I2C_ISR_STOPF; //PARA
    I2C2->CR2=0;//EL CR2 VUELVE A 0 PARA ENVIAR MAS DATOS
	
   
    I2C2->CR1 &= ~I2C_CR1_PE; // SE DESCATIVA EL ENABLE 
    while (I2C2->CR1 & I2C_CR1_PE);// SE COMPRUEBA QUE SE HAYA DESHABILITADO
    I2C2->TIMINGR |= 0x30420F13;             //TIMMING UTILIZADO PARA 100KHZ
    I2C2->CR2 &=~ I2C_CR2_ADD10; // SE HABILITA QUE SEA DE 7BITS
    I2C2->CR2 |= I2C_CR2_AUTOEND; // SE ACTIVA EL AUTOEND
    I2C2->CR1 |= I2C_CR1_ANFOFF; //SE DESHABILITA EL FILTRO ANALOGO
    I2C2->CR1 |= I2C_CR1_NOSTRETCH; //SE DESHABILITA EL NOSTRETCH
    I2C2->CR1 |= I2C_CR1_PE; // SE HABILITA EL ENABLR PARA EL I2C2
		
    I2C2->CR2 |= 0x020124D1; // EL CR2 SE MANTIEN IGUAL PERO LA DIRECCION SE CAMBIA PARA PODER ALMACENAR LOS DATOS RECIBIDOS 
    while (!(I2C2->ISR & I2C_ISR_RXNE)); // SE VALIDA QUE SE HABILITE EL CR2 Y SE REALICE LA RECEPCION
    Dato = I2C2->RXDR; // SE REALIZA LA RECEPCION 
    while (!(I2C2->ISR & I2C_ISR_STOPF));  // SE DA ESPERA AL BIT DE PARADA
    I2C2->ISR &= ~I2C_ISR_STOPF; //BIT DE PARADA
    I2C2->CR2=0; // EL CR2 VUELVE A 0 PARA OTRA TRANSMISION
     
    I2C2->CR1 &= ~I2C_CR1_PE; // SE DESHABILITA EL I2C2
    while (I2C2->CR1 & I2C_CR1_PE); // SE VALIDA QUE SE HAYA DESHABILITADO
    I2C2->TIMINGR |= 0x30420F13;             // TIMING DE 100KHZ
    I2C2->CR2 &=~ I2C_CR2_ADD10; // DIRECCION DE 7 BITS 
    I2C2->CR2 |= I2C_CR2_AUTOEND; // SE ACTIVA EL AUTOEND
    I2C2->CR1 |= I2C_CR1_ANFOFF; // SE DESACTIVA EL FILTRO ANALOGO
    I2C2->CR1 |= I2C_CR1_NOSTRETCH; // SE DESACTIVA EL NOSTRETCH
    I2C2->CR1 |= I2C_CR1_PE; // SE HABILITA EL I2C2
     
    return (Dato);
}
void I2C2_Lectura(void){
				//REGISTROS EN CONFIGURACION PARA EL GIROSCOPIO 
        for (i=0; i<10000; i++) {};		//OJO -> i=0; i<30000; i++
        X1 = I2C2_Read(0x3B);  //CAMBIAR 0X03, POR EL REGISTRO MSB EN X DEL MPU6050 -> CAMBIAR POR ACELEROMETRO
        for (i=0; i<10000; i++) {};
        X2 = I2C2_Read(0x3C);  //CAMBIAR 0X04, POR EL REGISTRO LSB EN X DEL MPU6050 -> CAMBIAR POR ACELEROMETRO
        for (i=0; i<10000; i++) {};
        Y1 = I2C2_Read(0x3D);  //CAMBIAR 0X07, POR EL REGISTRO MSB EN Y DEL MPU6050 -> CAMBIAR POR ACELEROMETRO
        for (i=0; i<10000; i++) {};
        Y2 = I2C2_Read(0x3E);  //CAMBIAR 0X08, POR EL REGISTRO LSB EN Y DEL MPU6050 -> CAMBIAR POR ACELEROMETRO
        for (i=0; i<10000; i++) {};
        Z1 = I2C2_Read(0x3F);  //CAMBIAR 0X05, POR EL REGISTRO MSB EN Z DEL MPU6050 -> CAMBIAR POR ACELEROMETRO
        for (i=0; i<10000; i++) {};
        Z2 = I2C2_Read(0x40);  //CAMBIAR 0X06, POR EL REGISTRO LSB EN Z DEL MPU6050 -> CAMBIAR POR ACELEROMETRO
        for (i=0; i<10000; i++) {};
                 		
					TX=X1;
					TY=Y1;
					TZ=Z1;
}
void I2C2_Descom(void){
  // poscicion 0 a 99 en x
	Nx=X1%100-0XFF00;    
		if(Nx>255){
		Nx=Nx-0x100;
	}
	// para obtener un valor de 2 digitos en hex  se realiza mood 100
	auxiliar=(Nx*0.388); // se reliza una escala de 0xFF- 0x00 -> 99-0
	Nx1=auxiliar/10;     // Nx1 contiene las decenas del digito posicion
	Nx2=auxiliar-(Nx1*10);// Nx2 contiene las unidades del digito posicion
	// poscion 0 a 99 en y
	Ny=Y1%100-0XFF00;           // para obtener un valor de 2 digitos en hex  se realiza mood 100
	if(Ny>255){
		Ny=Ny-0x100;
	}
	auxiliar=(Ny*0.388); // se reliza una escala de 0xFF- 0x00 -> 99-0
	Ny1=auxiliar/10;     // Nx1 contiene las decenas del digito posicion
	Ny2=auxiliar-(Ny1*10);// Nx2 contiene las unidades del digito posicion
	//posicion 0 a 99 en z
	Nz=Z1%100;           // para obtener un valor de 2 digitos en hex  se realiza mood 100
	if(Nz>0x00FF){
		Nz=Nz-0xFF00;
	}
	auxiliar=(Nz*0.388); // se reliza una escala de 0xFF- 0x00 -> 99-0
	Nz1=auxiliar/10;     // Nx1 contiene las decenas del digito posicion
	Nz2=auxiliar-(Nz1*10);// Nx2 contiene las unidades del digito posicion
	
	 send_comando(ddramlL);
		for(int i=0;i<5;i++){
			send_dato(posx[i]);
		}
		send_comando(ddramlL+5);
	  send_dato(numeros[Nx1]);
		send_comando(ddramlL+6);
	  send_dato(numeros[Nx2]);
		
	  send_comando(ddramlL+9);
		for(int i=0;i<5;i++){
			send_dato(posy[i]);
		}
		send_comando(ddramlL+14);
	  send_dato(numeros[Ny1]);
		send_comando(ddramlL+15);
	  send_dato(numeros[Ny2]);
		
		send_comando(ddram2L);
		for(int i=0;i<5;i++){
			send_dato(posz[i]);
		}
		send_comando(ddram2L+5);
	  send_dato(numeros[Nz1]);
		send_comando(ddram2L+6);
	  send_dato(numeros[Nz2]);
}

int main ()  {
	
	RCC->AHB1ENR |= 0x1A;	// SE HABILITAN LOS RELOJES B,D Y E
	GPIOD->MODER |=0X5555; // SE DECLARA EL MODER PARA LCD
	GPIOB->MODER |=0X45551000; // 
	
		SystemIn();
    SystemClock_Config();

    I2C2_Init();                  //SE INICIA EL CLOCK PARA EL I2C2
    RCC->AHB1ENR  |= 0x3F;   // SE ACTIVA EL CLOCK PARA  TODOS LOS PUERTOS
    GPIOD->MODER  |= 0x55555555;      // SE DA EL MODER PARA EL PUERTO D
	
	  I2C2_Write(0x6B,0x00);    //SE LLAMA LA FUNCION WRITE Y LECTURA PARA LA TRANSMISION DE DATOS
    for (i=0; i<10000; i++) {};
    I2C2_Write(0x1B,0x00);    //SE LLAMA LA FUNCION WRITE EN LOS PUERTOS DE CONFIG_GYRO 
    for (i=0; i<10000; i++) {};
    I2C2_Write(0x1C,0x00);		//SE LLAMA LA FUNCION WRITE EN LOS PUERTO DE CONFIG_ACELE
    for (i=0; i<10000; i++) {};
			
		GPIOE -> MODER |=0X55555; //LCD DEL 0-9 Y SUS SEND_COMANDO PARA FUNCIONAR
		send_comando(clear)
;
		send_comando(set);
	  send_comando(disp_on);
	  send_comando(mode);
	
  while(1) {

		I2C2_Lectura(); // SE LLAMA LA FUNCION DE RECEPCION 
		I2C2_Descom(); // SE LLAMA LA FUNCION DE DESCOMPOSICION
    for (i=0; i<10000; i++) {};   // tiempo de mas o menos 100ms 
  }
}
 
 
static void SystemClock_Config(void)
{
  RCC->CR |= ((uint32_t)RCC_CR_HSION);                     // SE DA EL ENABLE PARA EL CLOCK HSI/
  while ((RCC->CR & RCC_CR_HSIRDY) == 0);                  // ESPERA QUE SI SE ACTIVE EL CLOCK  /
 
  RCC->CFGR = RCC_CFGR_SW_HSI;                             // HSI DE SISTEMA DE CLOCK /
  while ((RCC->CFGR & RCC_CFGR_SWS) != RCC_CFGR_SWS_HSI);  // SE ESPERA QUE ES HSI USE EL CLOCK HABILITADO /
  RCC->CFGR |= (RCC_CFGR_HPRE_DIV1  |                      // SE CAMBIA  EL HCLK = SYSCLK /
                RCC_CFGR_PPRE1_DIV1 |                      // SE CAMBIA  EL APB1 = HCLK/2 /
                RCC_CFGR_PPRE2_DIV1  );                    // SE CAMBIA  EL APB2 = HCLK/1 /
  RCC->CR &= ~RCC_CR_PLLON;                                // SE DESHABILITA EL PLL PARA EL CLOCK  /
}

void SystemIn(void){ //FUNCION DE SYSTEMIN 
 int a=0;                         // SE DACLARA UNA VARIABLE A
 RCC->CR |= 0x10000;              // SE ACTIVA EL CR      
 while((RCC->CR & 0x20000)==0);   // SE DA ESPERA QUE SI SE ACTIVE EL CR           
 RCC->APB1ENR = 0x10080000;       // RE ACTIVA EL CLOCK DEL APB1ENR           
 RCC->CFGR = 0x00009400;                     
 RCC->PLLCFGR = 0x07405408;                  
 RCC->CR |= 0x01000000;                      
 while((RCC->CR & 0x02000000)==0);           
 FLASH->ACR = (0x00000605);                  
 RCC->CFGR |= 2;                             
 for (a=0;a<=500;a++);
}
//void initGPIO(void){
//	__HAL_RCC_GPIOB_CLK_ENABLE();
//	GPIO_InitTypeDef puertoX;
//	puertoX.Pin=GPIO_PIN_0|GPIO_PIN_11|GPIO_PIN_12|GPIO_PIN_15|GPIO_PIN_13;
//	puertoX.Mode=GPIO_MODE_OUTPUT_PP;
//	puertoX.Pull=GPIO_PULLUP;
//	puertoX.Speed=GPIO_SPEED_MEDIUM;
//	
//	HAL_GPIO_Init(GPIOB, &puertoX);
//}

//int main(void){
//	
//	initGPIO();
//	
//	LCD_setRST(GPIOB,GPIO_PIN_0);
//	LCD_setDC(GPIOB,GPIO_PIN_11);
//	LCD_setCE(GPIOB,GPIO_PIN_12);
//	LCD_setDIN(GPIOB,GPIO_PIN_15);
//	LCD_setCLK(GPIOB,GPIO_PIN_13);
//	
//	LCD_init();
//	
//	while(true){
//		
//		LCD_print("Hola Mundo!",0,0);

//	}
//	
//}