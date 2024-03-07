import socket
from AES import *
from ECC import *

skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 1234
skt.bind(('', port)) 
skt.listen(5)
key_len = 256
while True:
    print("Waiting for Connection")
    c, addr = skt.accept()	
    print ('Got connection from', addr )

    c.send(str(key_len).encode())
    print(c.recv(1024).decode())
    ecc = ECC(key_len)
    ecc.start_active()
    P,a,b,G = ecc.get_shared_params()

    print("p:",P)
    print("a:",a)
    print("b:",b)
    print("G.x:",G.x)
    print("G.y:",G.y)
   
    strs = str(P)+","+str(a)+","+str(b)+","+str(G.x)+","+str(G.y)
    c.send(strs.encode())
    print(c.recv(1024).decode())

    strs = c.recv(1024).decode().split(',')
    client_pub_key_x = int(strs[0])
    client_pub_key_y = int(strs[1])
    strs = str(ecc.get_public_key_own().x)+","+str(ecc.get_public_key_own().y)
    c.send(strs.encode())
    shared_key = ecc.start_shared_key(EllipticCurvePoint(client_pub_key_x,client_pub_key_y))
    print("Shared Key: ",shared_key.x)
    
    aes = AES(key_len)
    cipher = c.recv(1024).decode()

    hex_values = cipher.split(',')
    hex_list = [format(int(hex_value, 16),'02X') for hex_value in hex_values]
    pt,strs,t=aes.decryption_cbc(hex_list,str(shared_key.x))
    print("Decrypted text:",strs)

    strs = "ACK: Text Received"
    cipher,et,kst = aes.encryption_cbc(strs, str(shared_key.x)) 
    cipher = ",".join(cipher)
    c.send(cipher.encode())

    c.close()


