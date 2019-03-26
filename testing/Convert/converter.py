import base64

const = 492
def fileToBase64(filename):
    with open(filename, "rb") as image_file:
        image=image_file.read()
        encoded_string = base64.b64encode(image)
    return encoded_string.decode('utf-8')


def base64ToFile(encoded_string, outputFileName):
    data64decode = base64.decodestring(encoded_string.encode('utf-8'))
    data_result = open(outputFileName, "wb")
    data_result.write(data64decode)


def makeSingleString(bigList):
    retData = ""
    dollar = "$$$$$$$$$$$$$$$$$$$$$$$$$"
    for listEle in bigList:
        msg = str(listEle)
        msg = msg + dollar
        msg = msg[0:42]
        retData = retData + msg
    return retData


def makeListFromString(longString):
    retData = []
    data = longString.split('$')
    for item in data:
        if len(item) > 0:
            retData.append(int(item))
    return retData
