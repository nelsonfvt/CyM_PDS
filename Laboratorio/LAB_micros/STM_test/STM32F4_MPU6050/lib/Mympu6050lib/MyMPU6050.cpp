#include "MyMPU6050.h"
#include <i2c1.h>

void MPU_write(uint8_t addr, uint8_t reg, uint8_t data)
{
    Start_i2c1();
    Address_i2c1(addr);
    SendByte_i2c1(reg);
    SendByte_i2c1(data);
    Stop_i2c1();
}

void MPU_read(uint8_t addr, uint8_t reg, uint8_t * data)
{
    Start_i2c1();
    Address_i2c1(addr);
    SendByte_i2c1(reg);
    Start_i2c1();
    ReadByte_i2c1(addr+0x01, data);
    Stop_i2c1();
}

void MPU_read(uint8_t addr, uint8_t reg, uint8_t *data, uint8_t size)
{
    Start_i2c1();
    Address_i2c1(addr);
    SendByte_i2c1(reg);
    Start_i2c1();
    ReadBuff_i2c1(addr+0x01, data, size);
    Stop_i2c1();
}

void MPU_init()
{
    uint8_t check;
    uint8_t data;

    //verificando dispostivo
    MPU_read(MPU6050_ADDR,WHO_AM_I_REG, &check);

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

void MPU6050_Read_Accel (float * Ac_buff)
{
    uint8_t Rx_data[6];
    int16_t AcX_raw;
    int16_t AcY_raw;
    int16_t AcZ_raw;
	
	// Read 6 BYTES of data starting from ACCEL_XOUT_H register
    MPU_read(MPU6050_ADDR, ACCEL_XOUT_H_REG, Rx_data, 6);

    AcX_raw = (int16_t)(Rx_data[0] << 8 | Rx_data [1]);
    AcY_raw = (int16_t)(Rx_data[2] << 8 | Rx_data [3]);
    AcZ_raw = (int16_t)(Rx_data[4] << 8 | Rx_data [5]);

    //conversion a m/s^2
    float fact = 9.81 / 16384.0;
    Ac_buff[0] = AcX_raw * fact;
    Ac_buff[1] = AcY_raw * fact;
    Ac_buff[2] = AcZ_raw * fact;
}
void MPU6050_Read_Gyro (float *Gr_buff)
{
    uint8_t Rx_data[6];
    int16_t GrX_raw;
    int16_t GrY_raw;
    int16_t GrZ_raw;

    // Read 6 BYTES of data starting from GYRO_XOUT_H_REG register
    MPU_read(MPU6050_ADDR, GYRO_XOUT_H_REG, Rx_data, 6);

    GrX_raw = (int16_t)(Rx_data[0] << 8 | Rx_data [1]);
    GrY_raw = (int16_t)(Rx_data[2] << 8 | Rx_data [3]);
    GrZ_raw = (int16_t)(Rx_data[4] << 8 | Rx_data [5]);

    // convertir a rad/s
    float fact = (250.0 / 32768.0) * (3.141592 / 180.0);
    Gr_buff[0] = GrX_raw * fact;
    Gr_buff[1] = GrY_raw * fact;
    Gr_buff[2] = GrZ_raw * fact;
}