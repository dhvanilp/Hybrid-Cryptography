import random
from Curve import *
h = 1
k = random.getrandbits(256)

def encAscii(character):
	return ord(character)<<2

def decAscii(asciiVal):
	return  int(asciiVal)>>2

def encode(msg):
	encodedString = ''
	for i in msg:
		encodedString+=str(encAscii(i))
	return encodedString

def decode(encAscii_string):
	pack = ''
	i = 0
	decodedString = ''
	while (i < len(str(encAscii_string))):
		pack = encAscii_string[i:i+3]
		decodedString+=chr(decAscii(pack))
		i=i+3
	return decodedString;	

def modInverse(a,n=P): 
    lowM = 1
    highM = 0
    low = a%n
    high = n
    while low > 1:
        r = high/low
        nm = highM-lowM*r 
        new = high-low*r
        lowM, low, highM, high = nm, new, lowM, low
    return lowM % n

def eccAddition(a,b):
    LamAdd = ((b[1]-a[1]) * modInverse(b[0]-a[0],P)) % P
    x = (LamAdd*LamAdd-a[0]-b[0]) % P
    y = (LamAdd*(a[0]-x)-a[1]) % P
    return(x, y)

def ecTwoFold(a):
    Lam = ((3*a[0]*a[0]+A) * modInverse((2*a[1]),P)) % P
    x = (Lam*Lam-2*a[0]) % P
    y = (Lam*(a[0]-x)-a[1]) % P
    return(x, y)

def eccDot(generatedPoint,randomK): #Double & add. Not true multiplication
    randomKBin = str(bin(randomK))[2:]
    Q=generatedPoint

    for i in range (1, len(randomKBin)): #  EC multiplication.
        Q=ecTwoFold(Q)
        if randomKBin[i] == "1":
            Q=eccAddition(Q,generatedPoint)
    return (Q)

privKey = random.getrandbits(256)    

def gen_pubKey():
    #print("******* Public Key Generation *********")
    PublicKey = eccDot(GP, privKey)
    return PublicKey

message = raw_input("Enter Message to be encrypted > ")

def encryption(Public_Key, msg):
     
     C1 = eccDot(GP, k)
     C2 = eccDot(Public_Key, k)[0] + int(msg)

     return (C1, C2)

decrypted_string = ''

def decryption(C1, C2, private_Key):
    
     solution = C2-eccDot(C1, private_Key)[0]

     return (solution)

(C1,C2) = encryption(gen_pubKey(), encode(message))

decrypted_string = decryption(C1, C2, privKey)
s=decode(str(decrypted_string))

print("Cipher : ", C1, C2)
print("Original : ")
print(s)
