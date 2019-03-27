import base64
from PIL import Image


def fileToBase64(filename):
    with open(filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
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


def encodeStringinImage(data, output_file, type, width=512, height=512):
    data = data.encode('utf-8')
    print("This is lenght of the data in image:", len(data))
    image_data = []
    i = 0

    for y in range(height):
        for x in range(width):
            if(i+2 < len(data)):
                temp = (4*data[i], 2*data[i+1], 2*data[i+2])
                i = i+3
                image_data.append(temp)
            else:
                image_data.append((255, 255, 255))

    # print(image_data)
    img = Image.new('RGB',  (width, height))
    img_data = img.load()

    index = 0
    for y in range(height):
        for x in range(width):
            img_data[x, y] = image_data[index]
            index += 1

    img.save(output_file, type)
