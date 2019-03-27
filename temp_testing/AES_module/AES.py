import sys
from . import Constants


class AES:
    def __init__(self, key):
        self.shiftKey(key)

    def shiftKey(self, key):
        self.roundKey = self.inputMatrix(key)

        for i in range(4, 4 * 11):
            self.roundKey.append([])
            if i % 4 == 0:
                newKey = self.roundKey[i - 4][0] ^ Constants.Sbox[self.roundKey[i - 1]
                                                                  [1]] ^ Constants.Rcon[i // 4]
                self.roundKey[i].append(newKey)

                for j in range(1, 4):
                    newKey = self.roundKey[i -
                                           4][j] ^ Constants.Sbox[self.roundKey[i - 1][(j + 1) % 4]]
                    self.roundKey[i].append(newKey)
            else:
                for j in range(4):
                    newKey = self.roundKey[i - 4][j] ^ self.roundKey[i - 1][j]
                    self.roundKey[i].append(newKey)

    def encryption(self, plainText):
        self.plainState = self.inputMatrix(plainText)

        self.addRoundKey(self.plainState, self.roundKey[:4])

        for i in range(1, 10):
            self.substituteBytes(self.plainState)  # sub bytes
            self.rowShifter(self.plainState)  # shift rows
            self.columnMixer(self.plainState)  # mix column
            self.addRoundKey(
                self.plainState, self.roundKey[4 * i: 4 * (i + 1)])

        self.substituteBytes(self.plainState)
        self.rowShifter(self.plainState)
        self.addRoundKey(self.plainState, self.roundKey[40:])

        return self.matrixOutput(self.plainState)

    def decryption(self, cipherText):
        self.cipher_state = self.inputMatrix(cipherText)

        self.addRoundKey(self.cipher_state, self.roundKey[40:])
        self.inverseRowShifter(self.cipher_state)
        self.inverseSubstituteBytes(self.cipher_state)

        for i in range(9, 0, -1):
            self.addRoundKey(self.cipher_state,
                             self.roundKey[4 * i: 4 * (i + 1)])
            self.inverseColumnMixer(self.cipher_state)
            self.inverseRowShifter(self.cipher_state)
            self.inverseSubstituteBytes(self.cipher_state)

        self.addRoundKey(self.cipher_state, self.roundKey[:4])

        return self.matrixOutput(self.cipher_state)

    def addRoundKey(self, s, k):
        for i in range(4):
            for j in range(4):
                s[i][j] = s[i][j] ^ k[i][j]

    def substituteBytes(self, s):
        for i in range(4):
            for j in range(4):
                s[i][j] = Constants.Sbox[s[i][j]]

    def inverseSubstituteBytes(self, s):
        for i in range(4):
            for j in range(4):
                s[i][j] = Constants.InvSbox[s[i][j]]

    def rowShifter(self, shift):
        shift[0][1], shift[1][1], shift[2][1], shift[3][1] = shift[1][1], shift[2][1], shift[3][1], shift[0][1]
        shift[0][2], shift[1][2], shift[2][2], shift[3][2] = shift[2][2], shift[3][2], shift[0][2], shift[1][2]
        shift[0][3], shift[1][3], shift[2][3], shift[3][3] = shift[3][3], shift[0][3], shift[1][3], shift[2][3]

    def inverseRowShifter(self, iShift):
        iShift[0][1], iShift[1][1], iShift[2][1], iShift[3][1] = iShift[3][1], iShift[0][1], iShift[1][1], iShift[2][1]
        iShift[0][2], iShift[1][2], iShift[2][2], iShift[3][2] = iShift[2][2], iShift[3][2], iShift[0][2], iShift[1][2]
        iShift[0][3], iShift[1][3], iShift[2][3], iShift[3][3] = iShift[1][3], iShift[2][3], iShift[3][3], iShift[0][3]

    def columnMixer(self, state):
        for i in range(4):
            t = state[i][0] ^ state[i][1] ^ state[i][2] ^ state[i][3]
            u = state[i][0]
            state[i][0] ^= t ^ self.mixFactor(state[i][0] ^ state[i][1])
            state[i][1] ^= t ^ self.mixFactor(state[i][1] ^ state[i][2])
            state[i][2] ^= t ^ self.mixFactor(state[i][2] ^ state[i][3])
            state[i][3] ^= t ^ self.mixFactor(state[i][3] ^ u)

    def inverseColumnMixer(self, state):
        for i in range(4):
            u = self.mixFactor(self.mixFactor(state[i][0] ^ state[i][2]))
            v = self.mixFactor(self.mixFactor(state[i][1] ^ state[i][3]))
            state[i][0] ^= u
            state[i][1] ^= v
            state[i][2] ^= u
            state[i][3] ^= v

        self.columnMixer(state)

# referred from https://en.wikipedia.org/wiki/Rijndael_MixColumns
    def mixFactor(self, x):
        return (((x << 1) ^ 27) & 255) if (x & 128) else (x << 1)

    def inputMatrix(self, input):
        matrix = []
        for i in range(16):
            inputByte = (input >> (8 * (15 - i))) & 255
            if i % 4 == 0:
                matrix.append([inputByte])
            else:
                matrix[i // 4].append(inputByte)
        return matrix

    def matrixOutput(self, matrix):
        output = 0
        for i in range(4):
            for j in range(4):
                output |= (matrix[i][j] << (120 - (((i << 2) + j) << 3)))
        return output

    def encAscii(self, character):
        return ord(character) << 2

    def decAscii(self, asciiVal):
        return int(asciiVal) >> 2

    def encode(self, msg):
        encodedString = ''
        for i in msg:
            encodedString += str(self.encAscii(i))
        return encodedString

    def decode(self, encAscii_string):
        pack = ''
        i = 0
        decodedString = ''
        while (i < len(str(encAscii_string))):
            pack = encAscii_string[i:i+3]
            decodedString += chr(self.decAscii(pack))
            i = i+3
        return decodedString

    def breakIntoChunks(self, data):
        retData = []
        dataLen = len(data)
        for i in range(0, dataLen, 12):
            temp = data[i:i+12]
            retData.append(temp)
        return retData

    def chunksToData(self, chunks):
        retData = ""
        for i in chunks:
            retData = retData+i
        return retData

    def encryptBigData(self, data):
        chuck_data = self.breakIntoChunks(data)
        retData = []
        for chunk in chuck_data:
            encrypted_chunk = self.encryption(int(self.encode(chunk)))
            encrypted_chunk = int(encrypted_chunk)
            retData.append(encrypted_chunk)
        return retData

    def decryptBigData(self, encrypted_chunks):
        data=""
        for chunk in encrypted_chunks:
            decrypted_chunk = self.decode(str(self.decryption(chunk)))
            data=data+decrypted_chunk
        return data