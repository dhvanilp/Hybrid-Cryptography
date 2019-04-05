import base64
import os
import csv
import driver


def compareFile(inputFile, outputFile):
    with open(inputFile, "rb") as image_file:
        input_string = base64.b64encode(image_file.read())
    with open(outputFile, "rb") as image_file:
        output_string = base64.b64encode(image_file.read())

    len = 0
    match = 0
    for i, j in zip(input_string, output_string):
        len = len+1
        if i == j:
            match = match+1
    correct = match/len * 100
    loss = (len-match)/len*100
    return correct, loss


def main():
    original_images = "test_files/original/"
    generated_images = "test_files/generated/"

    with open('audio.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')

        filewriter.writerow(["original_file", "size_of_file", "loss_in_data","retain_data", "encrpyt_time", "decrypt_time"])

        monitor = 0
        for filename in os.listdir(original_images):
            monitor += 1
            print("No of images done:", monitor)
            image_path = original_images + filename
            output_path = generated_images+"generated_"+filename
            statinfo = os.stat(image_path)
            size_of_file = statinfo[6]
            encrypt_time, decrypt_time = driver.encrypt_and_decrypt(image_path, output_path)
            correct, loss  = compareFile(image_path, output_path)

            filewriter.writerow([filename, size_of_file, loss,
                                correct, encrypt_time, decrypt_time])


if __name__ == "__main__":
    main()
