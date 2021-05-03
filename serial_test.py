from threading import Thread, Event
from time import sleep
import serial
import socket
import sys

# serial comm constants
serial_comm = serial.Serial('COM4',9600)
serial_comm.timeout = 0.1

# tcp comm constants
server = "localhost"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# thread setup
event = Event()

# tcp bind
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def threaded_client(conn, var):
    welcome_str = "connected"
    conn.send(str.encode(welcome_str))
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            if not data:
                print("Disconnected")
                break
            else:
                # a="5"
                if data[0] == 0 and data[1] == 0:
                    a = "7"
                    var[0]=7
                if data[0] == 100 and data[1] == 0:
                    a = "8"
                    var[0]=8
                if data[0] == 200 and data[1] == 0:
                    a = "9"
                    var[0]=9
                if data[0] == 0 and data[1] == 100:
                    a = "4"
                    var[0]=4
                if data[0] == 100 and data[1] == 100:
                    a = "5"
                    var[0]=5
                if data[0] == 200 and data[1] == 100:
                    a = "6"
                    var[0]=6
                if data[0] == 0 and data[1] == 200:
                    a = "1"
                if data[0] == 100 and data[1] == 200:
                    a = "2"                                                                                                                        
                if data[0] == 200 and data[1] == 200:
                    a = "3"                                                                                                                        
                
                # print(a, data[0], data[1])


        except:
            break

        if event.is_set():
            break

    print("Lost connection")
    conn.close()

conn, addr = s.accept()
print("Connected to:", addr)


def threaded_serial_read(var):
    i=0
    while True:
        print(serial_comm.readline().decode('utf-8'))
        
        serial_comm.write(str.encode(str(var[0])))        
        for i in range(len(var)):
            var[i] += 1
        if event.is_set():
            break
        sleep(.5)
    print('Stop printing')


my_var = [1, 2, 3]

t = Thread(target=threaded_client, args=(conn, my_var, ))
t.start()

t2 = Thread(target=threaded_serial_read, args=(my_var, ))
t2.start()

while True:
    try:
        # print(my_var)
        # serial_comm.write(str(my_var[0]).encode())
        sleep(1)
    except KeyboardInterrupt:
        event.set()
        break
t.join()
print(my_var)



serial_comm.close()
