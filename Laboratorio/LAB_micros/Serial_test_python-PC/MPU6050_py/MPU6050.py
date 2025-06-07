import serial
import csv
import sys
import struct

class MPU6050_2_csv:
    def __init__(self, ser_port):
        self.ser_port = ser_port
        self.file_name = None
        self.n_samples = 0
        self.port_open = False
        self.values_list = []
        

    def connect(self):
        try:
            self.s_comm = serial.Serial(self.ser_port, baudrate=115200)
            self.port_open = True
            print("Puerto serial abierto")
        except IOError:
            print("Falló abrir el puerto serial " + self.ser_port)

    def disconnect(self):
        if self.port_open:
            self.s_comm.close()
            print("Puerto serial cerrado")


    def MPU_capture(self, n_samples):
        if self.port_open == True:
            self.n_samples = int(n_samples)
            print("Inicia captura de " + n_samples + " muestras")

            self.values_list = [None] * self.n_samples

            f = True
            cont = 0

            while f:
                t_list = [None] * 6
                band = self.s_comm.read()

                if band[0] == 97:

                    buff = self.s_comm.read(4)
                    ax = struct.unpack('f', buff[0:4])[0] # bytes a float
                    buff = self.s_comm.read(4)
                    ay = struct.unpack('f', buff[0:4])[0] # bytes a float
                    buff = self.s_comm.read(4)
                    az = struct.unpack('f', buff[0:4])[0] # bytes a float

                    buff = self.s_comm.read(4)
                    gx = struct.unpack('f', buff[0:4])[0] # bytes a float
                    buff = self.s_comm.read(4)
                    gy = struct.unpack('f', buff[0:4])[0] # bytes a float
                    buff = self.s_comm.read(4)
                    gz = struct.unpack('f', buff[0:4])[0] # bytes a float

                    t_list[0] = ax
                    t_list[1] = ay
                    t_list[2] = az

                    t_list[3] = gx
                    t_list[4] = gy
                    t_list[5] = gz

                    cont += 1
                    if cont == self.n_samples:
                        f = False
                    self.values_list[cont-1] = t_list
                



            # for n in range(0, self.n_samples):
            #     l = self.s_comm.readline()
            #     t_list = [None] * 6
            #     if l[0] == 97: # or l[0] == 103:
            #         ax = struct.unpack('f', l[1:5])[0] # bytes a float
            #         ay = struct.unpack('f', l[5:9])[0] # bytes a float
            #         az = struct.unpack('f', l[9:13])[0] # bytes a float

            #         gx = struct.unpack('f', l[13:17])[0] # bytes a float
            #         gy = struct.unpack('f', l[17:21])[0] # bytes a float
            #         gz = struct.unpack('f', l[21:25])[0] # bytes a float

            #         t_list[0] = ax
            #         t_list[1] = ay
            #         t_list[2] = az

            #         t_list[3] = gx
            #         t_list[4] = gy
            #         t_list[5] = gz

            #         print (t_list)
                    

        
        else:
            print("Puerto serial no abierto")

    def MPU_save(self, file_name):
        print("Guardando archivo...")
        self.file_name = file_name
        fields = ['AccX', 'AccY', 'AccZ', 'GyrX', 'GyrY', 'GyrZ']

        with open(self.file_name, 'w') as f:
            write = csv.writer(f)
            write.writerow(fields)
            write.writerows(self.values_list)
        print("Archivo: " + file_name + " guardado")



if __name__ == "__main__":
    print("Inicio...")

    if len(sys.argv) > 3:
        print("Tomando argumentos")
        file_name = sys.argv[1]
        port = sys.argv[2]
        n_samples = sys.argv[3]

        
        my_MPU = MPU6050_2_csv(port)
        my_MPU.connect()
        if my_MPU.port_open:
            my_MPU.MPU_capture(n_samples)
            my_MPU.MPU_save(file_name)
            my_MPU.disconnect()
    
    else:
        print("Faltan argumentos...")
        print("Uso:")
        print("python3 MPU6050.py archivo_csv puerto_serial numero_muestras")