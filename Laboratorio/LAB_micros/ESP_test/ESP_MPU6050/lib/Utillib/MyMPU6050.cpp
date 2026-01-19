#include "MyMPU6050.h"
#include <Arduino.h>

#define MPU6050_ADDR 0x68
#define SMPLRT_DIV_REG 0x19
#define GYRO_CONFIG_REG 0x1B
#define ACCEL_CONFIG_REG 0x1C
#define ACCEL_XOUT_H_REG 0x3B
#define TEMP_OUT_H_REG 0x41
#define GYRO_XOUT_H_REG 0x43
#define PWR_MGMT_1_REG 0x6B
#define WHO_AM_I_REG 0x75


void MPU_init()
{
    Wire.begin(); //inicializa I2C

    char check;
    char data;

    MPU_read(MPU6050_ADDR, WHO_AM_I_REG, &check); //Who I Am
    
    if(check == 104)
    {
        // power management register 0X6B we should write all 0's to wake the sensor up
        data = 0x00;
        MPU_write(MPU6050_ADDR, PWR_MGMT_1_REG, data);

        // Set DATA RATE of 1KHz by writing SMPLRT_DIV register
		data = 0x07;
		MPU_write(MPU6050_ADDR, SMPLRT_DIV_REG, data);
        
        // Set accelerometer configuration in ACCEL_CONFIG Register
		// XA_ST=0,YA_ST=0,ZA_ST=0, FS_SEL=0 -> ? 2g
		data = 0x00;
		MPU_write(MPU6050_ADDR, ACCEL_CONFIG_REG, data);

        // Set Gyroscopic configuration in GYRO_CONFIG Register
		// XG_ST=0,YG_ST=0,ZG_ST=0, FS_SEL=0 -> ? 250 ?/s
		data = 0x00;		
        MPU_write(MPU6050_ADDR, GYRO_CONFIG_REG, data);
    }

}

void MPU_write(char s_addr, char r_addr, char data)
{
    // Envia 1 byte
    Wire.beginTransmission(s_addr);
    Wire.write(r_addr);
    Wire.write(data);
    Wire.endTransmission();
}

void MPU_read(char s_addr, char r_addr, char * data)
{
    // Leer 1 byte
    Wire.beginTransmission(s_addr);
    Wire.write(r_addr);
    Wire.endTransmission();
    
    Wire.requestFrom(s_addr, 1);

    while(Wire.available())
        data[0] = Wire.read();

}

void MPU6050_Read_Accel (float *Ac_buff)
{
    int16_t AcX_raw;
    int16_t AcY_raw;
    int16_t AcZ_raw;

    Wire.beginTransmission(MPU6050_ADDR);
    Wire.write(ACCEL_XOUT_H_REG);
    Wire.endTransmission(false); //mantiene la comunicación

    Wire.requestFrom(MPU6050_ADDR, 6);

    AcX_raw = Wire.read() << 8 | Wire.read();
    AcY_raw = Wire.read() << 8 | Wire.read();
    AcZ_raw = Wire.read() << 8 | Wire.read();

    //conversion a m/s^2
    float fact = 9.81 / 16384.0;
    Ac_buff[0] = AcX_raw * fact;
    Ac_buff[1] = AcY_raw * fact;
    Ac_buff[2] = AcZ_raw * fact;

}
void MPU6050_Read_Gyro (float *Gr_buff)
{
    int16_t GrX_raw;
    int16_t GrY_raw;
    int16_t GrZ_raw;

    Wire.beginTransmission(MPU6050_ADDR);
    Wire.write(GYRO_XOUT_H_REG);
    Wire.endTransmission(false); //mantiene la comunicación

    Wire.requestFrom(MPU6050_ADDR, 6);

    GrX_raw = Wire.read() << 8 | Wire.read();
    GrY_raw = Wire.read() << 8 | Wire.read();
    GrZ_raw = Wire.read() << 8 | Wire.read();

    // convertir a rad/s
    float fact = (250.0 / 32768.0) * (3.141592 / 180.0);
    Gr_buff[0] = GrX_raw * fact;
    Gr_buff[1] = GrY_raw * fact;
    Gr_buff[2] = GrZ_raw * fact;
}