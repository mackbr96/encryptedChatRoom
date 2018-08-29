#client side for encrypted chat room
import socket
import select
import sys
from random import randrange
import random
from fractions import gcd 
import math
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from urllib2 import urlopen
import time
import itertools
import threading
#HERE IS THE CRYPTO STUFF

sys.setrecursionlimit(2000)
done = False #for the animation thread

#Testing stuff going on here

#print("UserName: ")
#userName = sys.stdin.readline()






'''_________________________________________________________________________________________________'''
#Crypto stuff under here
#AES UNDER HERE
class AESCipher(object):

    def __init__(self, key): 
        self.bs = 64
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self.padding(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self.removePadding(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def padding(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def removePadding(s):
        return s[:-ord(s[len(s)-1:])]


#RSA UNDER HERE

def miller_rabin(m):
    time.sleep(0.0001)
    a = random.randint(1,m-1)
  
    if(xpmod(a,m,m) != a): return False

    return True
 

def xpmod(a, b, m):
    time.sleep(0.0001)
    result = 1
    while b > 0:
        if b % 2 == 1:
            result = (result * a) % m
        a = (a * a) % m
        b = b // 2
    return result

def isprime(m,times):
    ''' Miller-Rabin's primality tester '''
    while times > 0:
        a = random.randrange(1,m)
        if xpmod(a,m,m) != a:
            return False
        times = times - 1
    return True


def generate_rsa_keys(bit_length,confidence):
    ''' Generate RSA keys with certain bit-length for the primes'''
    lower = pow(2,bit_length-1)
    upper = pow(2,bit_length)-1
    while True:
        p = random.randrange(lower,upper)
        if isprime(p,confidence):
            break
    return p


def pul(phi, e, Q, R, x1, y1, x2, y2):
    time.sleep(0.0001)
    x3 = x2
    y3 = y2
    y2 = y1 - Q*y2
   
    x2 = x1 - Q*x2
    x1 = x3
    y1 = y3
    R = phi%e
    if(R == 0): return y2
    Q = phi//e
    
    return pul(e, R,Q, R, x1, y1, x2, y2)

def pulverize(phi, e):
    '''Pulverizer algorithum'''
    Q = phi//e
    R = phi%e
    return pul(e,R,Q, R, 1,0,0,1)
    


def setUpRsa():
    '''Generates the RSA keys'''
    p = generate_rsa_keys(1024,20)
    q = generate_rsa_keys(1024,20)
    n = p*q

    phi = (p-1) * (q-1)

    e = 3
    g = gcd(e, phi)
    while (g != 1):
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    d = pulverize(phi, e)%phi

    return e,d,n


def animate():
    '''Animation function during loading'''
    animation = "|/-\\"
    i = 0
    while(done == False):
        anni = "\r" + "                    " + animation[i % len(animation)] + " LOADING " + animation[i % len(animation)] 
        sys.stdout.write(anni)
        sys.stdout.flush()
        i = i + 1
        time.sleep(0.08)
                
                

'''____________________________________________________________________________________________'''
#NETWORKING STUFF UNDER HERE

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_address = "192.168.1.29" #IP ADDRESS FOR SERVER
Port = 8027 #PORT OF SERVER
server.connect((IP_address, Port)) #connecting to the server
counter = 0
e = 0
d = 0
n = 0
AESkey = ""
unsecure = 1



myIP = urlopen('http://ip.42.pl/raw').read() #getting my ip to display as my name


while True:
    while(unsecure == 1):#aquiring the AES key
        sockets_list = [sys.stdin, server]
        
        read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
 
        for socks in read_sockets:
            if socks == server:
                message = socks.recv(2048)
                if(counter == 0):
                    print(message)
                    animateThread = threading.Thread(target=animate)
                    animateThread.start()
                    e,d,n = setUpRsa()
                    server.send(str(n) + "," + str(e))
                    counter = counter + 1
                elif(counter == 1):
                    done = True
                    print("")
                    print("              (*)AES KEY recieved(*)")
                    time.sleep(0.5)
                    
                    AESkey = str(pow(int(message),d,n))
            
                    print("(*)A secure connection has been aquired you may now chat(*)")
                    
                    safe = AESCipher(AESkey)
                    unsecure = 0


    #AFTER AES KEY AQUIRED
    sockets_list = [sys.stdin, server] #need this 
        
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])#need this!!
 
    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)

            

            #DECRYPT AES 
            message = safe.decrypt(message)
            
            
            if myIP not in message:    
                sys.stdout.write(message)
        else:
            message = sys.stdin.readline()
            
            
           

            message = "<" + myIP + ">" + message

            ##ENCRYPT AES STYLE
            message = safe.encrypt(message)
            
            server.send(message)

            
            sys.stdout.flush()
            

                        
server.close()
