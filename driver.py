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
    AES_tester()

    # AES_tester()
    # ECC_tester()
    # Converter_tester()

    #### 1. Multimedia data -> Base64 Encoding and plain text
    multimedia_data = converter.fileToBase64("test_files/test.jpg")


    # #### Encrypt  AES_key with ECC public key
    aes_key = 0x2b7e151628aed2a6abf7158809cf4f3c
    # # aes_key=str(aes_key)
    # ecc_AESkey = ECC.ECC()
    # privKey_for_aesKey = random.getrandbits(256)
    # publicKey_for_aesKey = ecc_AESkey.gen_pubKey(privKey_for_aesKey)
    # (C1_aesKey, C2_aesKey) = ecc_AESkey.encryption(publicKey_for_aesKey, str(aes_key))
    # # decryptedAESkey = ecc_AESkey.decryption(C1_aesKey,C2_aesKey, privKey_for_aesKey)

    #### 2. Encrypt the multimedia_data with AES algorithm
    aes_multimedia_data = AES.AES(aes_key)
    encrypted_multimedia = aes_multimedia_data.encryptBigData(multimedia_data)
    print("This is the encrypted data:", encrypted_multimedia)
    # decrypted_multimedia = aes_multimedia_data.decryptBigData(encrypted_multimedia)
    # print("This is the decrypted data:", decrypted_multimedia)
    #
    # #### 3. Encrypt the encrypted_multimedia with ECC
    # ecc_multimedia_data = ECC.ECC()
    # # here the same keys are used as before
    # (C1_multimedia, C2_multimedia) = ecc_multimedia_data.encryption(publicKey_for_aesKey, encrypted_multimedia)
    #
    # #### 5. Data to send to the other side:
    # # (C1_aesKey, C2_aesKey)
    # # (C1_multimedia, C2_multimedia)
    # # privKey_for_aesKey
    #
    #
    # ######################################################
    # ##### This is on the receiver side
    #
    # #### 1. Decrypt the data with ECC
    #
    # ecc_multimedia_dataD = ECC.ECC()
    # encrypted_multimedia = ecc_multimedia_dataD.decryption(C1_multimedia, C2_multimedia, privKey_for_aesKey)
    #
    # #### Decrypt with ECC to get the AES key
    # ecc_AESkey = ECC.ECC()
    # decryptedAESkey = ecc_AESkey.decryption(C1_aesKey,C2_aesKey, privKey_for_aesKey)
    #
    # #### 2. Decrypt with AES
    # aes_multimedia_data = AES.AES(decryptedAESkey)
    # decrypted_multimedia = aes.decryptBigData(encrypted_multimedia)
    #
    #
    # #### 3. Decode from Base64 to the corresponding fileToBase64
    # converter.base64ToFile(decrypted_multimedia, "success.jpg")










if __name__ == "__main__":
    main()
