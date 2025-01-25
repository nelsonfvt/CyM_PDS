import serial
import struct
import csv
import time
import sys


if __name__ == "__main__":
    print("Inicio...")

    if len(sys.argv) > 2:
        
        s_comm = serial.Serial(sys.argv[2], baudrate=115200,timeout=0.05)
        print("Puerto abierto.")
        csvfile = open(sys.argv[1])
        v_reader = csv.reader(csvfile, delimiter=',')

        next_call = time.time()
        for row in v_reader:
            # Formato de datos
            delim = str('_').encode()
            fin = str('\n').encode()
            dato1 = bytearray(struct.pack("f", float(row[0]))) # leyendo datos como flotantes
            dato2 = bytearray(struct.pack("f", float(row[1])))
            # concatenar
            buff = dato1 + delim + dato2 + fin
            
            #Enviar por puerto serial
            s_comm.write(buff)
            #Leyendo del puerto serial
            l = s_comm.readline()
            x = struct.unpack('f', l[0:4])[0] # bytes a float
            y = struct.unpack('f', l[4:8])[0]
            print("Envia: " + str(buff) + '\t' +"Recibe: " + str(x) + ' ' + str(y) + ' ' + "Suma: " + str((x+y)))
            #print(s_comm.readline())

            # Espera para enviar siguiente dato
            next_call = next_call + 0.1
            time.sleep(next_call - time.time())

        print("Final...")
        s_comm.close()
        print("Puerto cerrado.")

    else:
        print("Faltan argumentos...")
        print("Uso:")
        print("python3 send_data.py archivo_csv puerto_serial")