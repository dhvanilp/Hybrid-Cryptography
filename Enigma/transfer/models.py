from django.db import models
from .AES_module import AES
from .ECC_module import ECC
from .Convert import converter
import ast

class File(models.Model):
    sender = models.CharField(max_length=50)
    receiver = models.CharField(max_length=50)
    file = models.FileField(upload_to='transfer/uploads/')
    aes_key = models.CharField(max_length=40)
    ecc_public = models.CharField(max_length=350)
    file_type = models.CharField(max_length=5)

    C1_aesKey = models.CharField(max_length=350)
    C2_aesKey = models.CharField(max_length=350)

    C1_multimedia = models.CharField(max_length=350)
    C2_multimedia = models.CharField(max_length=350)

    def get_file_type(self):
        self.file_type = str(self.file).split(".")[1]

    def encrypt_AES_key(self):
        ecc_obj_AESkey = ECC.ECC()
        (self.C1_aesKey, self.C2_aesKey) = ecc_obj_AESkey.encryption(ast.literal_eval(self.ecc_public), str(int(self.aes_key)))

    def encrypt_multimedia(self):
        multimedia_data = converter.fileToBase64(str(self.file))
        aes = AES.AES(int(self.aes_key))
        encrypted_multimedia = aes.encryptBigData(multimedia_data)
        data_for_ecc = converter.makeSingleString(encrypted_multimedia)
        ecc = ECC.ECC()
        (self.C1_multimedia, self.C2_multimedia) = ecc.encryption(ast.literal_eval(self.ecc_public), data_for_ecc)

