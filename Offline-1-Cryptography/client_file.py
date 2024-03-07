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

#ECC Key Exchange started
ecc_key = ECC(key_len)
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
ecc_key.start_passive(P,a,b,G)
strs = str(ecc_key.get_public_key_own().x)+","+str(ecc_key.get_public_key_own().y)
skt.send(strs.encode())
strs = skt.recv(1024).decode().split(',')
server_pub_key_x = int(strs[0])
server_pub_key_y = int(strs[1])
shared_key = str(ecc_key.start_shared_key(EllipticCurvePoint(server_pub_key_x,server_pub_key_y)).x)
print("Shared Key: ",shared_key)
#ECC Key exchange ended
skt.send(str("ACK: Key Exchanged Succussfully").encode())
print("\nKey Exchanged Succussfully\n")

aes = AES(key_len)
f_len = int(skt.recv(1024).decode())
skt.send(str("ACK: File Lenght received Succussfully").encode())
print("file lenght:",f_len)
ciphers = ""
BUFFER_SIZE = 4096 * 10
while True:
  message = skt.recv(BUFFER_SIZE).decode()
  ciphers +=message
  if len(ciphers) == f_len:
    break
  
output_file = "client_received_file.txt"
hex_values = ciphers.split(',')
hex_list = [format(int(hex_value, 16),'02X') for hex_value in hex_values]
_,  dt = aes.decryption_file(hex_list, output_file, shared_key)
print("File received Succussfully")
skt.send(str("ACK: File received Succussfully").encode())
skt.close()





