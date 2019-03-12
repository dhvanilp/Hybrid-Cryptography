import random
import Hash

#secp256k1

Pcurve = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 -1 # The proven prime

#Elliptic curve: y^2 = x^3 + Acurve * x + Bcurve
Acurve = 0; Bcurve = 7

#Generator Point
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
GPoint = (Gx,Gy) 

#Number of points in the field [Order of G]
N=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141 

h = 01  #Cofactor
k = random.getrandbits(256)

def modinv(a,n=Pcurve): #Extended Euclidean Algorithm/'division' in elliptic curves
    lm, hm = 1,0
    low, high = a%n,n
    while low > 1:
        ratio = high/low
        nm, new = hm-lm*ratio, high-low*ratio
        lm, low, hm, high = nm, new, lm, low
    return lm % n

def ECadd(a,b):  #Elliptic curve addition
    LamAdd = ((b[1]-a[1]) * modinv(b[0]-a[0],Pcurve)) % Pcurve
    x = (LamAdd*LamAdd-a[0]-b[0]) % Pcurve
    y = (LamAdd*(a[0]-x)-a[1]) % Pcurve
    return (x,y)

def ECdouble(a): # Point doubling,invented for EC
    Lam = ((3*a[0]*a[0]+Acurve) * modinv((2*a[1]),Pcurve)) % Pcurve
    x = (Lam*Lam-2*a[0]) % Pcurve
    y = (Lam*(a[0]-x)-a[1]) % Pcurve
    return (x,y)

def EccMultiply(GenPoint,ScalarHex): #Double & add. Not true multiplication 
    if ScalarHex == 0 or ScalarHex >= N: 
	raise Exception("Invalid Scalar/Private Key")
    ScalarBin = str(bin(ScalarHex))[2:]
    Q=GenPoint
    for i in range (1, len(ScalarBin)): #  EC multiplication.
        Q=ECdouble(Q)
        if ScalarBin[i] == "1":
            Q=ECadd(Q,GenPoint)
    return (Q)

privKey = random.getrandbits(256)    

def gen_pubKey():
    #print("******* Public Key Generation *********")
    PublicKey = EccMultiply(GPoint, privKey)

    return PublicKey


message = raw_input("Enter Message to be encrypted > ")

def encryption(Public_Key, msg):
     C1 = EccMultiply(GPoint, k)
     C2 = EccMultiply(Public_Key, k)[0] + int(msg)
     return (C1, C2)

decrypted_string = ''

def decryption(C1, C2, private_Key):  
     solution = C2-EccMultiply(C1, private_Key)[0]
     return (solution)

(C1,C2) = encryption(gen_pubKey(), Hash.encode(message))

decrypted_string = decryption(C1, C2, privKey)
s=Hash.decode(str(decrypted_string))

print("Cipher Text : ", C1, C2)
print("-----")
print(" **Original Message** ")
print(s)
