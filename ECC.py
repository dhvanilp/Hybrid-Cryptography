import random
import Hash

#secp521r1

Pcurve = int(0x1ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff)
#Elliptic curve: y^2 = x^3 + Acurve * x + Bcurve
Acurve = 6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057148L
Bcurve = 1093849038073734274511112390766805569936207598951683748994586394495953116150735016013708737573759623248592132296706313309438452531591012912142327488478985984L

#Generator Point
Gx = int(0x0c6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66)
Gy = int(0x11839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650)
GPoint = (Gx,Gy) 

#Number of points in the field [Order of G]
N=0x1fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa51868783bf2f966b7fcc0148f709a5d03bb5c9b8899c47aebb6fb71e91386409 

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
