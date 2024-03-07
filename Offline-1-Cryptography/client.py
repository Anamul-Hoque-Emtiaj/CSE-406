import socket
from AES import *
from ECC import *

skt = socket.socket()		
port = 1234			
skt.connect(('127.0.0.1', port))

msg = skt.recv(1024).decode()
key_len = int(msg)
print("Key Length:",key_len)
skt.send(str("ACK: Received Key length").encode())

ecc = ECC(key_len)
strs = skt.recv(1024).decode().split(',')
P = int(strs[0])
a = int(strs[1])
b = int(strs[2])
x = int(strs[3])
y = int(strs[4])
print("p:",P)
print("a:",a)
print("b:",b)
print("G.x:",x)
print("G.y:",y)
skt.send(str("ACK: Received shared_Params").encode())

G = EllipticCurvePoint(x,y)
ecc.start_passive(P,a,b,G)
strs = str(ecc.get_public_key_own().x)+","+str(ecc.get_public_key_own().y)
skt.send(strs.encode())
strs = skt.recv(1024).decode().split(',')
server_pub_key_x = int(strs[0])
server_pub_key_y = int(strs[1])
shared_key = ecc.start_shared_key(EllipticCurvePoint(server_pub_key_x,server_pub_key_y))
print("Shared Key: ",shared_key.x)

aes = AES(key_len)
plain_text = input("Enter the text:")
cipher,et,kst = aes.encryption_cbc(plain_text, str(shared_key.x)) 
cipher = ",".join(cipher)
skt.send(cipher.encode())

cipher = skt.recv(1024).decode()
hex_values = cipher.split(',')
hex_list = [format(int(hex_value, 16),'02X') for hex_value in hex_values]
pt,strs,t = aes.decryption_cbc(hex_list,str(shared_key.x))
print("Decrypted text:",strs)

skt.close()
