import sys

Sbox = (
    99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118,
    202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192,
    183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21,
    4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117,
    9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132,
    83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207,
    208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168,
    81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210,
    205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115,
    96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219, 224,
    50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121, 231,
    200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8, 186,
    120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138, 112,
    62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158, 225,
    248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223, 140,
    161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22
    )

InvSbox = (
    82, 9, 106, 213, 48, 54, 165, 56, 191, 64, 163, 158, 129, 243, 215, 251,
    124, 227, 57, 130, 155, 47, 255, 135, 52, 142, 67, 68, 196, 222, 233,
    203, 84, 123, 148, 50, 166, 194, 35, 61, 238, 76, 149, 11, 66, 250, 195,
    78, 8, 46, 161, 102, 40, 217, 36, 178, 118, 91, 162, 73, 109, 139, 209,
    37, 114, 248, 246, 100, 134, 104, 152, 22, 212, 164, 92, 204, 93, 101,
    182, 146, 108, 112, 72, 80, 253, 237, 185, 218, 94, 21, 70, 87, 167, 141,
    157, 132, 144, 216, 171, 0, 140, 188, 211, 10, 247, 228, 88, 5, 184, 179,
    69, 6, 208, 44, 30, 143, 202, 63, 15, 2, 193, 175, 189, 3, 1, 19, 138,
    107, 58, 145, 17, 65, 79, 103, 220, 234, 151, 242, 207, 206, 240, 180,
    230, 115, 150, 172, 116, 34, 231, 173, 53, 133, 226, 249, 55, 232, 28, 117,
    223, 110, 71, 241, 26, 113, 29, 41, 197, 137, 111, 183, 98, 14, 170, 24,
    190, 27, 252, 86, 62, 75, 198, 210, 121, 32, 154, 219, 192, 254, 120, 205,
    90, 244, 31, 221, 168, 51, 136, 7, 199, 49, 177, 18, 16, 89, 39, 128, 236,
    95, 96, 81, 127, 169, 25, 181, 74, 13, 45, 229, 122, 159, 147, 201, 156,
    239, 160, 224, 59, 77, 174, 42, 245, 176, 200, 235, 187, 60, 131, 83, 153,
    97, 23, 43, 4, 126, 186, 119, 214, 38, 225, 105,20, 99, 85, 33, 12, 125
    )

Rcon = (0, 1, 2, 4, 8, 16, 32, 64, 128, 27, 54, 108, 216, 171, 77, 154, 47, 94, 188, 99, 198, 151, 53, 106, 212, 179, 125, 250, 239, 197, 145, 57)


class AES:
    def __init__(self, master_key):
        self.shiftKey(master_key)

    def shiftKey(self, master_key):
        self.roundKey = inputMatrix(master_key)

        for i in range(4, 4 * 11):
            self.roundKey.append([])
            if i % 4 == 0:
                byte = self.roundKey[i - 4][0]        \
                     ^ Sbox[self.roundKey[i - 1][1]]  \
                     ^ Rcon[i // 4]
                self.roundKey[i].append(byte)

                for j in range(1, 4):
                    byte = self.roundKey[i - 4][j]    \
                         ^ Sbox[self.roundKey[i - 1][(j + 1) % 4]]
                    self.roundKey[i].append(byte)
            else:
                for j in range(4):
                    byte = self.roundKey[i - 4][j]    \
                         ^ self.roundKey[i - 1][j]
                    self.roundKey[i].append(byte)


    def encrypt(self, plaintext):
        self.plainState = inputMatrix(plaintext)

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

    def decrypt(self, ciphertext):
        self.cipher_state = inputMatrix(ciphertext)

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
                s[i][j] ^= k[i][j]

    def substituteBytes(self, s):
        for i in range(4):
            for j in range(4):
                s[i][j] = Sbox[s[i][j]]


    def inverseSubstituteBytes(self, s):
        for i in range(4):
            for j in range(4):
                s[i][j] = InvSbox[s[i][j]]


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
        inputByte = (input >> (8 * (15 - i))) & 0xFF
        if i % 4 == 0:
            matrix.append([inputByte])
        else:
            matrix[i // 4].append(inputByte)
    return matrix

def matrixOutput(matrix):
    output = 0
    for i in range(4):
        for j in range(4):
            output |= (matrix[i][j] << (120 - 8 * (4 * i + j)))
    return output


def main():
    if len(sys.argv)!=2:
        print "Choose either encryption or decryption as follows: "
        print "python aes.py encrypt // python aes.py decrypt"
        exit()

    master_key = 0x2b7e151628aed2a6abf7158809cf4f3c
    aes = AES(master_key)

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
