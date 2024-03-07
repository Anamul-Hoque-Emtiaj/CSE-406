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

    #ECC for key exchange started
    ecc_key = ECC(key_len)
    ecc_key.start_active()
    P,a,b,G = ecc_key.get_shared_params()
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
    strs = str(ecc_key.get_public_key_own().x)+","+str(ecc_key.get_public_key_own().y)
    c.send(strs.encode())
    shared_key = str(ecc_key.start_shared_key(EllipticCurvePoint(client_pub_key_x,client_pub_key_y)).x)
    print("Shared Key: ",shared_key)
    #ECC for key exchange ended
    print(c.recv(1024).decode())
    
    aes = AES(key_len)
    file_path = "file1.txt"
    cipher_text, _, _ = aes.encryption_file(file_path, shared_key)
    cipher_text_str = ",".join(cipher_text)
    print(len(cipher_text))
    print(len(cipher_text_str))
    c.send(str(len(cipher_text_str)).encode())
    print(c.recv(1024).decode())
    c.send(cipher_text_str.encode())

    print(c.recv(1024).decode())

    c.close()