import serial
import csv
import sys

class MPU6050_2_csv:
    def __init__(self, ser_port, file_name):
        self.ser_port = ser_port
        self.file_name = file_name
        self.n_samples = 0
        self.port_open = False
        

    def connect(self):
        try:
            self.s_comm = serial.Serial(self.ser_port, baudrate=115200,timeout=0.05)
            self.port_open = True
            print("Puerto serial abierto")
        except IOError:
            print("No se abrio el puerto")


    def MPU_capture(self, n_samples):
        if self.port_open == True:
            self.n_samples = n_samples
            print("inicia captura")
        
        else:
            print("Puerto serial no abierto")




if __name__ == "__main__":
    print("Inicio...")

    if len(sys.argv) > 3:
        print("Tomando argumentos")
        file_name = sys.argv[1]
        port = sys.argv[2]
        n_samples = sys.argv[3]

        
        my_MPU = MPU6050_2_csv(port, file_name)
        my_MPU.connect()
        my_MPU.MPU_capture(n_samples)
    
    else:
        print("Faltan argumentos...")
        print("Uso:")
        print("python3 send_data.py archivo_csv puerto_serial numero_muestras")