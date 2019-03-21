import sys
import random
from AES_module import AES
from ECC_module import ECC
from Convert import converter


def AES_tester():
    msg = input("Enter the text to be encrypted > ")

    key = 0x2b7e151628aed2a6abf7158809cf4f3c

    aes = AES.AES(key)

    dataE = aes.encryptBigData(msg)
    print("This is the encrypted data:", dataE)

    dataD = aes.decryptBigData(dataE)
    print("This is the decrypted data:", dataD)


def ECC_tester():
    message = input("Enter Message to be encrypted > ")

    privKey = random.getrandbits(256)

    ecc = ECC.ECC()
    public_key = ecc.gen_pubKey(privKey)

    (C1, C2) = ecc.encryption(public_key, message)
    print("This is the encrypted data, Cipher (C1,C2): ")
    print("C1(x,y) is: ", C1)
    print("C2(x,y) is: ", C2)

    dataD = ecc.decryption(C1, C2, privKey)
    print("This is the decrypted dataginal : ", dataD)


def Converter_tester():
    data = converter.fileToBase64("test_files/test.jpg")
    converter.base64ToFile(data, "test_success.jpg")


def main():

    # AES_tester()
    # ECC_tester()
    # Converter_tester()

    # 1. Multimedia data -> Base64 Encoding and plain text
    multimedia_data = converter.fileToBase64("test_files/test.jpg")

    # 2. Encrypt  AES_key with ECC public key
    aes_key = 0x2b7e151628aed2a6abf7158809cf4f3c
    ecc_AESkey = ECC.ECC()
    privKey_for_aesKey = random.getrandbits(256)
    publicKey_for_aesKey = ecc_AESkey.gen_pubKey(privKey)
    (C1_aesKey, C2_aesKey) = ecc_AESkey.encryption(publicKey_for_aesKey, aes_key)
    
    # decryptedAESkey = ecc_AESkey.decryption(C1_aesKey,C2_aesKey, privKey_for_aesKey)
    


if __name__ == "__main__":
    main()
