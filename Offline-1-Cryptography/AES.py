from BitVector import *
from threading import Thread
import os
import time

# Tables for AES
Sbox = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

InvSbox = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)

Mixer = [
    [BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03")],
    [BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02")]
]

InvMixer = [
    [BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09")],
    [BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D")],
    [BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B")],
    [BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E")]
]

# Global variables
ROUND_COUNT = {128 : 10, 192 : 12, 256 : 14}
AES_modulus = BitVector(bitstring='100011011')
debug = True
# circular left shift list
def circuler_left_shift_1d(li,shift):
    return li[shift:] + li[:shift]

# circular right shift list
def circuler_right_shift_1d(li,shift):
    return li[-shift:] + li[:-shift]

# XOR 2 list
def xor_1d(l1,l2):
    return [l1[i]^l2[i] for i in range(0,len(l1))]

# circular left shift matrix
def circuler_left_shift_2d(mat):
    for i in range(0,len(mat)):
        mat[i] = circuler_left_shift_1d(mat[i],i)
    return mat

# circular right shift matrix
def circuler_right_shift_2d(mat):
    for i in range(0,len(mat)):
        mat[i] = circuler_right_shift_1d(mat[i],i)
    return mat

# XOR 2 matrix
def xor_matrix(m1,m2):
    mat = []
    for i in range(0,len(m1)):
        mat.append(xor_1d(m1[i],m2[i]))
    return mat
# convert string to hex
def string_to_hex_list(input_string):
    hex_list = [format(ord(char), '02X') for char in input_string]    
    return hex_list

# convert hex_list to 2d array
def hex_list_to_2d_array(hex_list):
    return [hex_list[i:i+4] for i in range(0, len(hex_list), 4)]

# convert string to 2d Bitvector array
def convert_string_to_bitvector_array(input_string):
    hex_list = string_to_hex_list(input_string)
    return convert_list_to_bitvector_array(hex_list)
    
# convert Hex List(Cypher) to 2d Bitvector array
def convert_list_to_bitvector_array(input_list):
    arr = hex_list_to_2d_array(input_list)
    transposed_list = [[row[i] for row in arr] for i in range(len(arr[0]))]
    bitvector_array = [[BitVector(hexstring=hex_value) for hex_value in row] for row in transposed_list]
    return bitvector_array


# 2d column major Bitvector to 1d list
def bitvector_array_to_list(bitvector_array):
    # Flatten the column-major 2D array to a 1D list of BitVector objects
    flat_bitvector_list = [element for column in zip(*bitvector_array) for element in column]

    # Convert each BitVector to its hexadecimal representation
    hex_list = [bit_vector.getHexStringFromBitVector() for bit_vector in flat_bitvector_list]

    return hex_list

def gen_IV(len):
    return os.urandom(len)

class AES:
    def __init__(self, AES_LEN):
        self.AES_LEN = AES_LEN
        self.__round_keys = []
        self.__round_count = ROUND_COUNT[AES_LEN]

    def __generate_round_keys(self):
        self.__round_keys = []
        round_0 = convert_string_to_bitvector_array(self.__key)
        col = self.AES_LEN//32
        for  i in range(0,4):
            round_0[i] = round_0[i][0:col]
        self.__round_keys.append(round_0)
        
        round_constant = BitVector(hexstring="01")
        for round in range(1,self.__round_count+1):
            lastRow = []
            for i in range(4):
                lastRow.append(self.__round_keys[round-1][i][col-1]) 
            lastRow = self.__g_of_(lastRow,round_constant)

            cur_key = []
            for i in range(0,col):
                prev_row = []
                for j in range(4):
                    prev_row.append(self.__round_keys[round-1][j][i])
                prev_row = xor_1d(prev_row,lastRow)
                cur_key.append(prev_row)
                lastRow = prev_row
            

            transposed_key = []
            for i in range(4):
                row = []
                for j in range(col):
                    row.append(cur_key[j][i])
                transposed_key.append(row)
            self.__round_keys.append(transposed_key)
            round_constant = round_constant.gf_multiply_modular(BitVector(hexstring="02"),AES_modulus,8)
    
    def __resize_key(self, key):
        key_len = self.AES_LEN
        if key_len < len(key):
            key = key[:key_len]
        else:
            key = key + "0"*(key_len-len(key))
        return key
    def __mix_columns(self,mat):
        m = []
        for _ in range(len(mat)):
            m.append([BitVector(intVal=0, size=8)] * len(mat[0]))
        for i in range(0,len(mat)):
            for j in range(0,len(mat[i])):
                for k in range(0,len(mat)):
                    m[i][j] ^=  (self.__mixer[i][k].gf_multiply_modular( mat[k][j],AES_modulus,8))
                    
        return m
    def __substitute_bytes_1d(self, li):
        return [BitVector(intVal=self.__sbox[li[i].intValue()],size=8) for i in range(0,len(li))]
    def __substitute_bytes_2d(self, mat):
        for i in range(0,len(mat)):
            mat[i] = self.__substitute_bytes_1d(mat[i])
        return mat
    def __g_of_(self,word,round_constant):
        word = circuler_left_shift_1d(word,1)
        sbox = self.__sbox
        self.__sbox = Sbox
        word = self.__substitute_bytes_1d(word)
        self.__sbox = sbox
        word[0] = word[0] ^ round_constant
        return word
    def __encryption_round(self, msg):
        msg_array = convert_list_to_bitvector_array(msg)
        state = xor_matrix(msg_array,self.__round_keys[0])
        for round in range(1,self.__round_count+1):
            state = self.__substitute_bytes_2d(state)
            state = circuler_left_shift_2d(state)
            if round != self.__round_count:
                state = self.__mix_columns(state)
            state = xor_matrix(state,self.__round_keys[round])
        return state
    def encryption(self, input_string, key):
        self.__key = self.__resize_key(key)
        self.__mixer = Mixer
        self.__sbox = Sbox
        start_time = time.time()
        self.__generate_round_keys()
        key_schedule_time = time.time() - start_time

        while( len(input_string)%(self.AES_LEN//8) != 0 ):
            input_string += '\x00'

        cipher_text = []
        start_time = time.time()
        for i in range(0,len(input_string),self.AES_LEN//8):
            split_text = input_string[i:i+self.AES_LEN//8]
            state = self.__encryption_round(string_to_hex_list(split_text))
            cipher_text.extend( bitvector_array_to_list(state))
        
        encryption_time = time.time() - start_time
        return cipher_text, encryption_time, key_schedule_time
    
    def __debug(self, state):
        if debug:
            for a in state:
                for b in a:
                    print(b.getHexStringFromBitVector(), end=' ')
                print("\n")
            print("\n")
   
    def __decryption_round(self, li):
        msg_array = convert_list_to_bitvector_array(li)
        state = xor_matrix(msg_array, self.__round_keys[0])

        for round in range(1, self.__round_count + 1):
            state = circuler_right_shift_2d(state)  # Inverse Shift Row
            state = self.__substitute_bytes_2d(state)
            state = xor_matrix(state, self.__round_keys[round])
            if round != self.__round_count:
                state = self.__mix_columns(state)
        return state

    
    def decryption(self, cipher_text, key):
        self.__key = self.__resize_key(key)
        self.__mixer = InvMixer
        self.__sbox = InvSbox
        self.__generate_round_keys()
        li = self.__round_keys[::-1]
        self.__round_keys = li
        
        plain_text = []    
        start_time = time.time()
    
        for i in range(0,len(cipher_text),self.AES_LEN//8):
            split_text = cipher_text[i:i+self.AES_LEN//8]
            state = self.__decryption_round(split_text)
            plain_text.extend(bitvector_array_to_list(state))

        decryption_time = time.time() - start_time

        ascii_chars = [chr(int(hex_value, 16)) for hex_value in plain_text if hex_value != '00']
        result_string = ''.join(ascii_chars)
        return plain_text,result_string,decryption_time
    
    def __pad(self, data):
        pad_length = (self.AES_LEN // 8) - (len(data) % (self.AES_LEN // 8))
        padding = [format(pad_length, '02X') for _ in range(pad_length)]
        return data + padding

    def __unpad(self, data):
        pad_length =  int(data[-1], 16)
        return data[:-pad_length]
        
    def encryption_cbc(self, plaintext, key,li = False):
        self.__key = self.__resize_key(key)
        self.__mixer = Mixer
        self.__sbox = Sbox
        start_time = time.time()
        self.__generate_round_keys()
        key_schedule_time = time.time() - start_time

        iv = gen_IV(self.AES_LEN//8).hex()
        iv = [iv[i:i+2] for i in range(0, len(iv), 2)]  
        if not li:
            hex_list = string_to_hex_list(plaintext)
        else:
            hex_list = plaintext
        hex_list = iv + hex_list
        hex_list = self.__pad(hex_list)
        int_list = [int(val,16) for val in hex_list]

        cipher_text = []
        iv = [int(0) for _ in range(self.AES_LEN//8)]  # Initialization Vector (IV)
        start_time = time.time()
        for i in range(0, len(int_list), self.AES_LEN // 8):
            block = int_list[i:i + self.AES_LEN // 8]
            block = xor_1d(block, iv)
            block = [format(i,'02X') for i in block]
            encrypted_block = self.__encryption_round(block)
            cipher_text.extend( bitvector_array_to_list(encrypted_block))
            iv = [int(val,16) for val in bitvector_array_to_list(encrypted_block)]
        encryption_time = time.time()-start_time
        return cipher_text,encryption_time,key_schedule_time

    def decryption_cbc(self, ciphertext, key):
        self.__key = self.__resize_key(key)
        self.__mixer = InvMixer
        self.__sbox = InvSbox
        self.__generate_round_keys()
        li = self.__round_keys[::-1]
        self.__round_keys = li

        plaintext = []
        iv = [int(0) for _ in range(self.AES_LEN//8)]  # Initialization Vector (IV)

        start_time = time.time()
        for i in range(0, len(ciphertext), self.AES_LEN // 8):
            block = ciphertext[i:i + self.AES_LEN // 8]
            decrypted_block = self.__decryption_round(block)
            decrypted_block_int = [int(val,16) for val in bitvector_array_to_list(decrypted_block)]
            state = xor_1d(decrypted_block_int, iv)
            state = [format(i,'02X') for i in state]
            if i!=0:
                plaintext.extend(state)
            iv = [int(val,16) for val in block]

        plaintext = self.__unpad(plaintext)
        ascii_chars = [chr(int(hex_value, 16)) for hex_value in plaintext ]
        result_string = ''.join(ascii_chars)
        decryption_time = time.time()-start_time

        return plaintext,result_string,decryption_time
    
    def __ctr_round(self,nonce,out_li,counter,block): #threading

        state = self.__encryption_round(nonce[1:])
        state_int_list = [int(val,16) for val in bitvector_array_to_list(state)]
        if len(block) == len(state_int_list):
            xor = xor_1d(block,state_int_list)
        else:
            xor = xor_1d(block,state_int_list[:len(block)])
        
        xor = [format(val,'02X') for val in xor]
        out_li.insert(counter,xor)
    
    def encryption_ctr(self, li, key, nonce):
        self.__key = self.__resize_key(key)
        self.__mixer = Mixer
        self.__sbox = Sbox
        start_time = time.time()
        self.__generate_round_keys()
        key_schedule_time = time.time() - start_time

        counter = 0
        int_list = [int(val,16) for val in li]
        cipher_text = []

        thread = []
        start_time = time.time()
        for i in range(0, len(int_list), self.AES_LEN // 8):
            if i + self.AES_LEN // 8 <= len(int_list):
                block = int_list[i:i + self.AES_LEN // 8]
            else:
                block = int_list[i:]

            new_nonce_hex = hex(int(nonce,16)+counter)
            new_nonce_list = [new_nonce_hex[i:i+2] for i in range(0, len(new_nonce_hex), 2)]
            t = Thread(target=self.__ctr_round,args=(new_nonce_list,cipher_text,counter,block,))
            t.start()
            thread.append(t)
            counter +=1
        
        for t in thread:
            t.join()
        
        cipher = []
        for ci in cipher_text:
            cipher.extend(ci)
        
        encryption_time = time.time()-start_time
        return cipher,encryption_time,key_schedule_time
    def decryption_ctr(self, li, key, nonce):
        plain_text,dt,kst = self.encryption_ctr(li,key,nonce)
        ascii_chars = [chr(int(hex_value, 16)) for hex_value in plain_text ]
        result_string = ''.join(ascii_chars)
        return plain_text,result_string,dt
    
    def encryption_file(self, input_file, key):
        with open(input_file, 'rb') as file:
            plaintext_bytes = file.read()

        plaintext_hex = [format(byte, '02X') for byte in plaintext_bytes]

        return self.encryption_cbc(plaintext_hex, key,True)
    def decryption_file(self, cipher, output_file, key):
        plain_text,str,dt = self.decryption_cbc(cipher,key)
        plain_text_bytes = bytes([int(val,16) for val in plain_text])
        with open(output_file, 'wb') as file:
            file.write(plain_text_bytes)

        return file,dt


def list_to_string(li):
    return ' '.join(li)        

def task1():

    key = "BUET CSE19 Batch"
    plain_text = "Never Gonna Give you up"
    aes_len = 256
    iv = gen_IV(aes_len//8).hex()

    print("Key:")
    print("In Ascii:", key)
    print("In Hex:", list_to_string(string_to_hex_list(key)))
    print("\nPlain Text:")
    print("In Ascii:", plain_text)
    print("In Hex:", list_to_string(string_to_hex_list(plain_text)))

    aes = AES(aes_len)
    #cipher,et,kst = aes.encryption(plain_text, key) # ecb encryption
    #cipher,et,kst = aes.encryption_cbc(plain_text, key) # cbc encryption
    cipher,et,kst = aes.encryption_ctr(string_to_hex_list(plain_text), key, iv) # ctr encryption
    print("\nCiphered Text:")
    print("In Hex:",list_to_string(cipher))
    ascii_chars = [chr(int(hex_value, 16)) for hex_value in cipher ]
    result_string = ''.join(ascii_chars)
    try:
        print("In Ascii:", result_string)
    except UnicodeEncodeError:
        for char in result_string:
            try:
                print(char, end='')
            except UnicodeEncodeError:
                pass
    #hex,str,dt = aes.decryption(cipher, key) # ecb decryption
    #hex,str,dt = aes.decryption_cbc(cipher, key) # cbc decryption
    hex,str,dt = aes.decryption_ctr(cipher, key, iv) # ctr decryption

    print("\n\nDeciphered Text:")
    print("In Hex:",list_to_string(hex))
    print("In Ascii:", str)

    print("\nExecution time details:")
    print("Key Schedule Time: {:.4f} ms".format(kst * 1000))
    print("Encryption Time: {:.4f} ms".format(et * 1000))
    print("Decryption Time: {:.4f} ms".format(dt * 1000))

task1()



