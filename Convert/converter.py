import base64


def fileToBase64(filename):
    with open(filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string.decode('utf-8')


def base64ToFile(encoded_string, outputFileName):
    data64decode = base64.decodestring(encoded_string.encode('utf-8'))
    data_result = open(outputFileName, "wb")
    data_result.write(data64decode)
