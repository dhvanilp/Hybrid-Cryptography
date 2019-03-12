import base64

with open("image.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
print(encoded_string)