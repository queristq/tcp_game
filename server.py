import socket
from _thread import *
import sys
import serial

run_flag = True

serial_comm = serial.Serial('COM4',9600)
serial_comm.timeout = 0.1

server = "localhost"
port = 5556

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

pos = [(0,0),(100,100)]

def threaded_client(conn, player, run_flag):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                print("Received: ", data)
                print("Sending : ", reply)
                
            conn.sendall(str.encode(make_pos(reply)))
            
            # a="5"
            # if reply[0] == "0" and reply[1] == "0" :
            #      a = "7"
            # if reply[0] == "0" and reply[1] == "100" :
            #      a = "8"

            # serial_comm.write(str.encode(make_pos(a)))

        except:
            break

    print("Lost connection")
    conn.close()
    run_flag = False
    print (run_flag)

currentPlayer = 0


# def threaded_serial_read(count):
#     while True: 
#         count = count + 1
#         print ( count )
#         if ( count == 100):
#             break
#         try:
#             print(serial_comm.readline().decode('utf-8'))
#         except:
#             break

# start_new_thread(threaded_serial_read,(1,))

# while True:

conn, addr = s.accept()
print("Connected to:", addr)

start_new_thread(threaded_client, (conn, currentPlayer, run_flag, ))
while run_flag:
    print(run_flag) 
currentPlayer += 1
