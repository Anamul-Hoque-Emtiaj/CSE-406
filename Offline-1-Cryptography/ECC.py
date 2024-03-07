from BitVector import *
import random
import time



def generate_prime(bits):
    bv = BitVector(intVal = 0)
    primality = 0
    while primality < 0.999 or bv.intValue()<=3:
        bv = bv.gen_random_bits(bits)  
        primality = bv.test_for_primality()
    return bv.intValue()

class EllipticCurvePoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class ECC:
    def __init__(self,bits):
        self.__bits = bits
        self.__shared_params = {}
        self.__private_key = None
        self.__public_key_own = None
        self.__public_key_other = None
        self.__shared_key = None
    
    
    def __point_addition(self,P, Q, a, p):
        
        if P is None:
            return Q
        if Q is None:
            return P
        
        if P.x == Q.x and P.y != Q.y:
            return None
  

        if P != Q:
            slope = (Q.y - P.y) * pow(Q.x - P.x, -1, p) % p
        else:
            slope = (3 * P.x**2 + a) * pow(2 * P.y, -1, p) % p

        x = (slope**2 - P.x - Q.x) % p
        y = (slope * (P.x - x) - P.y) % p

        return EllipticCurvePoint(x, y)
    def __point_doubling(self,P, a, p):
        if P is None:
            return None  

        slope = (3 * P.x**2 + a) * pow(2 * P.y, -1, p) % p
        x = (slope**2 - 2 * P.x) % p
        y = (slope * (P.x - x) - P.y) % p

        return EllipticCurvePoint(x, y)
    def __scalar_multiplication(self,k, P, a, p):
        Q = None  

        k_binary = bin(k)[2:]

        for bit in k_binary:
            Q = self.__point_doubling(Q, a, p)
            if bit == '1':
                Q = self.__point_addition(Q, P, a, p)

        return Q
    def gen_shared_params(self):

        p = generate_prime(self.__bits)
        while True:
            a = random.randrange(0, p)
            x = random.randrange(0, p)
            y = random.randrange(0, p)
            b = (y**2 - x**3 - a*x) % p
            if 4*a**3 + 27*b**2 != 0:
                break
        
        self.__shared_params['P'] = p
        self.__shared_params['a'] = a
        self.__shared_params['b'] = b
        self.__shared_params['G'] = EllipticCurvePoint(x,y)
    
    def get_shared_params(self):
        return self.__shared_params['P'],self.__shared_params['a'],self.__shared_params['b'],self.__shared_params['G']
    def set_shared_params(self,P,a,b,G):
        self.__shared_params['P'] = P
        self.__shared_params['a'] = a
        self.__shared_params['b'] = b
        self.__shared_params['G'] = G

    def get_public_key_own(self):
        return self.__public_key_own
    
    def set_public_key_other(self,public_key_other):
        self.__public_key_other = public_key_other

    def get_shared_key(self):     
        return self.__shared_key
    
    def select_private_key(self):
        p = self.__shared_params['P']
        e = p+1-2*p**0.5
        self.__private_key = random.randint(2, e-1)

    def generate_public_key(self):
        self.__public_key_own = self.__scalar_multiplication(self.__private_key, self.__shared_params['G'], self.__shared_params['a'], self.__shared_params['P'])

    def generate_shared_key(self):
        self.__shared_key = self.__scalar_multiplication(self.__private_key, self.__public_key_other, self.__shared_params['a'], self.__shared_params['P'])
    
    def start_active(self):
        self.gen_shared_params()
        self.select_private_key()
        self.generate_public_key()
    def start_passive(self, P,a,b,G):
        self.set_shared_params(P,a,b,G)
        self.select_private_key()
        self.generate_public_key()
    
    def start_shared_key(self, other_public_key):
        self.set_public_key_other(other_public_key)
        self.generate_shared_key()
        return self.__shared_key



def task2():
    key_lens = [128,192,256]
    _time = []
    for key_len in key_lens:
        ta = 0
        tb = 0
        tr = 0
        for i in range(5):
            ECC1 = ECC(key_len)
            ECC2 = ECC(key_len)

            start_time = time.time()
            ECC1.start_active()
            ta+=(time.time()-start_time)

            P,a,b,G = ECC1.get_shared_params()
            start_time = time.time()
            ECC2.start_passive(P,a,b,G)
            tb+=(time.time()-start_time)

            start_time = time.time()
            ECC1.start_shared_key(ECC2.get_public_key_own())
            tr+=(time.time()-start_time)
        
        _time.append([200*ta,200*tb,200*tr])
    
    print("\n\nKey_len -- A -- B -- R")
    print("128 --",_time[0][0],"--",_time[0][1],"--",_time[0][2])
    print("192 --",_time[1][0],"--",_time[1][1],"--",_time[1][2])
    print("256 --",_time[2][0],"--",_time[2][1],"--",_time[2][2])

#task2()









