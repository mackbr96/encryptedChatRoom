# SERVER FOR ENCRYPTED CHAT ROOM
import socket
import select
import sys
from thread import *
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
import random

def setUpKey():
    key = ""
    for x in range(0, 20):
        key = key + chr(random.randint(0,127))
    return key

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


AESkey = setUpKey()
IP_address = "192.168.1.29" #YOUR IP
Port = 8028 #PORT YOU WISH TO USE
server.bind((IP_address, Port))


server.listen(100)
list_of_clients = []

def clientthread(conn, addr):
    conn.send("(*)Establishing a secure connection please wait(*)")
    unsecure = 1;
    while(unsecure == 1):#setting up the keys
        try:

            message = conn.recv(2048)
            if (message):
                m = message.split(',')
                n,e = m
                n = int(n)
                e = int(e)
                bits =  ''.join(format(ord(x), '08b') for x in AESkey)
                bits = int(bits, 2)

                conn.send(str(pow(bits, e, n)))
                unsecure = 0 #RSA KEYS AQUIRED NOW SECURE
        except:
            continue


    while True: #after keys are exchanged
            try:
                message = conn.recv(2048)
                if message:
                    print ("<" + addr[0] + "> " + message)
                    broadcast(message, conn)
                else:
                    remove(conn)
            except:
                continue

def broadcast(message, connection):#send to all clients
    for clients in list_of_clients:
        if clients!=connection:
            try:
                if(clients != a):
                    clients.send(message)
            except:
                clients.close()

while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print (addr[0] + " connected")
    start_new_thread(clientthread,(conn,addr))

conn.close()
server.close()
