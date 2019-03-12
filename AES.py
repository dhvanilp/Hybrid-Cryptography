import sys
import AES_helper

class AES:
    def __init__(self, key):
        self.shiftKey(key)

    def shiftKey(self, key):
        self.roundKey = inputMatrix(key)

        for i in range(4, 4 * 11):
            self.roundKey.append([])
            if i % 4 == 0:
                newKey = self.roundKey[i - 4][0]        \
                     ^ AES_helper.Sbox[self.roundKey[i - 1][1]]  \
                     ^ AES_helper.Rcon[i // 4]
                self.roundKey[i].append(newKey)

                for j in range(1, 4):
                    newKey = self.roundKey[i - 4][j]    \
                         ^ AES_helper.Sbox[self.roundKey[i - 1][(j + 1) % 4]]
                    self.roundKey[i].append(newKey)
            else:
                for j in range(4):
                    newKey = self.roundKey[i - 4][j]    \
                         ^ self.roundKey[i - 1][j]
                    self.roundKey[i].append(newKey)


    def encrypt(self, plainText):
        self.plainState = inputMatrix(plainText)

        self.addRoundKey(self.plainState, self.roundKey[:4])

        for i in range(1, 10):           
            self.substituteBytes(self.plainState)
            self.rowShifter(self.plainState)
            self.columnMixer(self.plainState)
            self.addRoundKey(self.plainState, self.roundKey[4 * i : 4 * (i + 1)])

        self.substituteBytes(self.plainState)
        self.rowShifter(self.plainState)
        self.addRoundKey(self.plainState, self.roundKey[40:])

        return matrixOutput(self.plainState)

    def decrypt(self, cipherText):
        self.cipher_state = inputMatrix(cipherText)

        self.addRoundKey(self.cipher_state, self.roundKey[40:])
        self.inverseRowShifter(self.cipher_state)
        self.inverseSubstituteBytes(self.cipher_state)

        for i in range(9, 0, -1):
            self.addRoundKey(self.cipher_state, self.roundKey[4 * i : 4 * (i + 1)])
            self.inverseColumnMixer(self.cipher_state)
            self.inverseRowShifter(self.cipher_state)
            self.inverseSubstituteBytes(self.cipher_state)

        self.addRoundKey(self.cipher_state, self.roundKey[:4])

        return matrixOutput(self.cipher_state)

    def addRoundKey(self, s, k):
        for i in range(4):
            for j in range(4):
                s[i][j] = s[i][j] ^  k[i][j]

    def substituteBytes(self, s):
        for i in range(4):
            for j in range(4):
                s[i][j] = AES_helper.Sbox[s[i][j]]


    def inverseSubstituteBytes(self, s):
        for i in range(4):
            for j in range(4):
                s[i][j] = AES_helper.InvSbox[s[i][j]]


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
            state[i][0] ^= t ^ mixFactor(state[i][0] ^ state[i][1])
            state[i][1] ^= t ^ mixFactor(state[i][1] ^ state[i][2])
            state[i][2] ^= t ^ mixFactor(state[i][2] ^ state[i][3])
            state[i][3] ^= t ^ mixFactor(state[i][3] ^ u)


    def inverseColumnMixer(self, state):
        for i in range(4):
            u = mixFactor(mixFactor(state[i][0] ^ state[i][2]))
            v = mixFactor(mixFactor(state[i][1] ^ state[i][3]))
            state[i][0] ^= u
            state[i][1] ^= v
            state[i][2] ^= u
            state[i][3] ^= v

        self.columnMixer(state)

def mixFactor(x):
    return (((x << 1) ^ 27) & 255) if (x & 128) else (x << 1)

def inputMatrix(input):
    matrix = []
    for i in range(16):
        inputByte = (input >> (8 * (15 - i))) & 255
        if i % 4 == 0:
            matrix.append([inputByte])
        else:
            matrix[i // 4].append(inputByte)
    return matrix

def matrixOutput(matrix):
    output = 0
    for i in range(4):
        for j in range(4):
            output |= (matrix[i][j] << (120 - (((i << 2) + j) << 3)))
    return output


def main():
    if len(sys.argv)!=2:
        print "Choose either encryption or decryption as follows: "
        print "python aes.py encrypt // python aes.py decrypt"
        exit()

    key = 0x2b7e151628aed2a6abf7158809cf4f3c
    aes = AES(key)

    if sys.argv[1]=="encrypt":
        # plaintext=int(hex(int(input("Enter the text to be encrypted: "))),0)
        plaintext = 0x3243f6a8885a308d313198a2e0370734
        encrypted = aes.encrypt(plaintext)

        print(plaintext)
        print(encrypted)
    elif sys.argv[1]=="decrypt":
        # ciphertext=int(hex(int(input("Enter the text to be decrypted: "))),0)
        ciphertext = 0x3925841d02dc09fbdc118597196a0b32
        decrypted = aes.decrypt(ciphertext)

        print(ciphertext)
        print(decrypted)


if __name__ == "__main__":
    main()
