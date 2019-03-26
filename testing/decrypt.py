import sys
import random
import json
from AES_module import AES
from ECC_module import ECC
from Convert import converter
import ast

def main():
    with open('.cipher.jpg') as f:
        data = json.load(f)
    # input_file = input("Enter the name of file to decrypt> ")
    # data = converter.fileToBase64(input_file)[532:]
    # temp =
    # for i in range(len(data),0,-1):
    #     if data[i]=='=':

    # print(json.loads(data))
    C1_aesKey = data["C1_aesKey"]
    C2_aesKey = data["C2_aesKey"]
    private_key = data["private_key"]
    file_type = data["file_type"]
    # This is on the receiver side

    ######################################################################################
    # Decrypt with ECC to get the AES key
    ecc_AESkey = ECC.ECC()
    decryptedAESkey = ecc_AESkey.decryption(C1_aesKey, C2_aesKey, private_key)
    ######################################################################################

    C1_multimedia = data["C1_multimedia"]
    C2_multimedia = data["C2_multimedia"]
    ######################################################################################
    # 1. Decrypt the data with ECC
    ecc_obj = ECC.ECC()
    encrypted_multimedia = ecc_obj.decryption(C1_multimedia, C2_multimedia, private_key)
    clean_data_list = converter.makeListFromString(encrypted_multimedia)
    ######################################################################################

    ######################################################################################
    # 2. Decrypt with AES
    # aes_multimedia_data = AES.AES(int(hex(int(decryptedAESkey)),0))
    aes_obj = AES.AES(int(decryptedAESkey))
    decrypted_multimedia = aes_obj.decryptBigData(clean_data_list)
    ######################################################################################

    ######################################################################################
    # 3. Decode from Base64 to the corresponding fileToBase64
    output_file = "test."+file_type
    converter.base64ToFile(decrypted_multimedia, output_file)
    delete = int(input("Delete File? 1/0:"))
    if(delete):
        import os
        os.remove(output_file)
    ######################################################################################


if __name__ == "__main__":
    main()