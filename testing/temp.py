# data =str(cipher).encode('utf-8')
    # altchars=b'+/'

    # data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    # missing_padding = len(data) % 4
    # if missing_padding:
    #     data += b'='* (4 - missing_padding)

    # converter.base64ToFile(data.decode('utf-8'), "cipher."+file_type)


import base64

with open("test_files/nitk.jpg", "rb") as image_file:
    image=image_file.read()
    file_sig = image[:3]
    print(image)
    
    # print(encoded_string)