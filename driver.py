import sys
import random
from AES_module import AES
from ECC_module import ECC
from Convert import converter


def main():
    # _______________________________________________
    # AES tester

    key = 0x2b7e151628aed2a6abf7158809cf4f3c
    aes = AES.AES(key)
    msg = raw_input("Enter the text to be encrypted: ")

    encrypted = aes.encryption(int(aes.encode(msg)))
    ciphertext = int(encrypted)
    print aes.encode(msg)
    print str(aes.decryption(ciphertext))
    decrypted = aes.decode(str(aes.decryption(ciphertext)))
    print "Decrypted(Original) Text is:"
    print(decrypted)

# # _______________________________________________
# # _______________________________________________
# ECC tester
    ecc = ECC.ECC()
    privKey = random.getrandbits(256)
    message = raw_input("Enter Message to be encrypted > ")

    decrypted_string = ''
    (C1, C2) = ecc.encryption(ecc.gen_pubKey(privKey), ecc.encode(message))

    decrypted_string = ecc.decryption(C1, C2, privKey)
    s = ecc.decode(str(decrypted_string))

    print "\nCipher (C1,C2): "
    print "\nC1(x,y) is: ", C1
    print "\nC2(x,y) is: ", C2
    print "\nOriginal : "
    print s
# # _______________________________________________
#     data = converter.fileToBase64("test_files/test.jpg")
#     # print data
#     converter.base64ToFile(data,"tesasat.jpg")


if __name__ == "__main__":
    main()
