import sys
import random
import time
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
    data = converter.fileToBase64("test_files/image.jpg")
    # print(data)
    converter.base64ToFile(data, "test_success.jpg")


def encrypt_and_decrypt(input_file,output_file):
    # AES_tester()
    # ECC_tester()
    # Converter_tester()

    # VERBOSE = int(input("VERBOSE 1/0? > "))
    VERBOSE = 0
    start_time = time.time()

    # input_file = input(
    #     "Enter the name of file to encrypt present in ./test_files/ > ")
    # output_file = input("Enter the name of output file > ")

    ######################################################################################
    # 1. Multimedia data -> Base64 Encoding and plain text
    multimedia_data = converter.fileToBase64(input_file)
    # multimedia_data = (b"hey").decode('utf-8')
    # multimedia_data = input("Enter the data >")
    ######################################################################################

    aes_key = 0x2b7e151628aed2a6abf7158809cf4f3c

    ######################################################################################
    # Encrypt  AES_key with ECC public key
    ecc_obj_AESkey = ECC.ECC()
    private_key = random.getrandbits(256)
    public_key = ecc_obj_AESkey.gen_pubKey(private_key)
    (C1_aesKey, C2_aesKey) = ecc_obj_AESkey.encryption(public_key, str(aes_key))
    # decryptedAESkey = ecc_AESkey.decryption(C1_aesKey,C2_aesKey, private_key)
    ######################################################################################

    ######################################################################################
    # 2. Encrypt the multimedia_data with AES algorithm
    aes = AES.AES(aes_key)
    encrypted_multimedia = aes.encryptBigData(multimedia_data)
    data_for_ecc = converter.makeSingleString(encrypted_multimedia)
    if(VERBOSE):
        print("######################################################################################")
        print("AES ENCRYPTION")
        print("Encrypted data from AES:", encrypted_multimedia)
        print("String data that is passed to ECC:", data_for_ecc)

    # converter.base64ToFile(decrypted_multimedia.encode('utf-8'),"test_success.jpg")
    ######################################################################################

    ######################################################################################
    # 3. Encrypt the encrypted_multimedia with ECC
    ecc = ECC.ECC()
    (C1_multimedia, C2_multimedia) = ecc.encryption(public_key, data_for_ecc)
    if(VERBOSE):
        print("######################################################################################")
        print("ECC ENCRYPTION")
        print("Encrypted data from ECC (C1,C2):")
        print("C1:", C1_multimedia)
        print("C2:", C2_multimedia)
    ######################################################################################

    ######################################################################################
    # Data to send to the other side:
    # (C1_aesKey, C2_aesKey)
    # (C1_multimedia, C2_multimedia)
    # private_key
    ######################################################################################

    middle_time = time.time()
    # This is on the receiver side

    ######################################################################################
    # Decrypt with ECC to get the AES key
    ecc_AESkey = ECC.ECC()
    decryptedAESkey = ecc_AESkey.decryption(C1_aesKey, C2_aesKey, private_key)
    if(VERBOSE):
        print("######################################################################################")
        print("AES key decrypted:", decryptedAESkey)
        print(type(decryptedAESkey))
    ######################################################################################

    ######################################################################################
    # 1. Decrypt the data with ECC
    ecc_obj = ECC.ECC()
    encrypted_multimedia = ecc_obj.decryption(
        C1_multimedia, C2_multimedia, private_key)
    clean_data_list = converter.makeListFromString(encrypted_multimedia)
    if(VERBOSE):
        print("######################################################################################")
        print("ECC Decryption")
        print("ECC Decryption from decrpytion:", encrypted_multimedia)
        print("Clean data from ECC decrpytion:", clean_data_list)
    ######################################################################################

    ######################################################################################
    # 2. Decrypt with AES
    # aes_multimedia_data = AES.AES(int(hex(int(decryptedAESkey)),0))
    aes_obj = AES.AES(int(decryptedAESkey))
    decrypted_multimedia = aes_obj.decryptBigData(clean_data_list)
    if(VERBOSE):
        print("######################################################################################")
        print("AES Decryption")
        print("Data original:", decrypted_multimedia)
        type(decrypted_multimedia)
    ######################################################################################

    ######################################################################################
    # 3. Decode from Base64 to the corresponding fileToBase64
    converter.base64ToFile(decrypted_multimedia, output_file)
    # delete = int(input("Delete File? 1/0:"))
    # if(delete):
    #     import os
        # os.remove(output_file)
    end_time = time.time()
    ######################################################################################

    encrypt_time = middle_time-start_time
    decrpyt_time = end_time-middle_time

    return round(encrypt_time,3),round(decrpyt_time,3)
