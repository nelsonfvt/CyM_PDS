#include "MyMPU6050.h"
#include <my_i2c.h>



#define MPU6050_ADDR 0xD0
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
    uint8_t check;
    uint8_t data;

    //Configura I2C1
    Configura_i2c2();

    //verificando dispostivo
    MPU_read(MPU6050_ADDR, WHO_AM_I_REG, &check); //Who I Am

    if(check == 104)
    {
        // power management register 0X6B we should write all 0's to wake the sensor up
        data = 0;
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

void MPU_read(uint8_t s_addr, uint8_t r_addr, uint8_t *data)
{
    SendByte_i2c2(s_addr, r_addr);
    ReadByte_i2c2(s_addr, data);
    
}

void MPU_write(uint8_t s_addr, uint8_t r_addr, uint8_t data)
{
    SendByte_i2c2(s_addr, r_addr);
    SendByte_i2c2(s_addr, data);
}

void MPU6050_Read_Accel (float *Ac_buff)
{
    int16_t AcX_raw;
    int16_t AcY_raw;
    int16_t AcZ_raw;
	

    uint8_t v1;
    uint8_t v2;
	// Read 6 BYTES of data starting from ACCEL_XOUT_H register
    MPU_read(MPU6050_ADDR, ACCEL_XOUT_H_REG, &v1);
    MPU_read(MPU6050_ADDR, ACCEL_XOUT_H_REG+0x01, &v2);
    
    AcX_raw = (int16_t)(v1 << 8 | v2);

    MPU_read(MPU6050_ADDR, ACCEL_XOUT_H_REG+0x02, &v1);
    MPU_read(MPU6050_ADDR, ACCEL_XOUT_H_REG+0x03, &v2);
    AcY_raw = (int16_t)(v1 << 8 | v2);

    MPU_read(MPU6050_ADDR, ACCEL_XOUT_H_REG+0x04, &v1);
    MPU_read(MPU6050_ADDR, ACCEL_XOUT_H_REG+0x05, &v2);
    AcZ_raw = (int16_t)(v1 << 8 | v2);

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

    uint8_t v1;
    uint8_t v2;
    // Read 6 BYTES of data starting from GYRO_XOUT_H_REG register
    MPU_read(MPU6050_ADDR, GYRO_XOUT_H_REG, &v1);
    MPU_read(MPU6050_ADDR, GYRO_XOUT_H_REG+0x01, &v2);
    GrX_raw = (int16_t)(v1 << 8 | v2);

    MPU_read(MPU6050_ADDR, GYRO_XOUT_H_REG+0x02, &v1);
    MPU_read(MPU6050_ADDR, GYRO_XOUT_H_REG+0x03, &v2);
    GrY_raw = (int16_t)(v1 << 8 | v2);

    MPU_read(MPU6050_ADDR, GYRO_XOUT_H_REG+0x04, &v1);
    MPU_read(MPU6050_ADDR, GYRO_XOUT_H_REG+0x05, &v2);
    GrZ_raw = (int16_t)(v1 << 8 | v2);

    // convertir a rad/s
    float fact = (250.0 / 32768.0) * (3.141592 / 180.0);
    Gr_buff[0] = GrX_raw * fact;
    Gr_buff[1] = GrY_raw * fact;
    Gr_buff[2] = GrZ_raw * fact;
}