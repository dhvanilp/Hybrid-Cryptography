import sys
import random
from AES_module import AES
from ECC_module import ECC
from Convert import converter


def main():

    # # _______________________________________________
    # AES tester
    msg = input("Enter the text to be encrypted > ")

    key = 0x2b7e151628aed2a6abf7158809cf4f3c

    aes = AES.AES(key)

    dataE = aes.encryptBigData(msg)
    print("This is the encrypted data:", dataE)

    dataD = aes.decryptBigData(dataE)
    print("This is the decrypted data:", dataD)


    # # _______________________________________________
    # # _______________________________________________
# ECC tester
    message = input("Enter Message to be encrypted > ")
    
    privKey = random.getrandbits(256)
    
    ecc = ECC.ECC()
    public_key = ecc.gen_pubKey(privKey)

    (C1, C2) = ecc.encryption(public_key, message)

    dataD = ecc.decryption(C1, C2, privKey)

    print("Cipher (C1,C2): ")
    print("C1(x,y) is: ", C1)
    print("C2(x,y) is: ", C2)
    print("Original : ",dataD)
# # _______________________________________________
#     data = converter.fileToBase64("test_files/test.jpg")
#     # print data
#     converter.base64ToFile(data,"tesasat.jpg")

if __name__ == "__main__":
    main()
