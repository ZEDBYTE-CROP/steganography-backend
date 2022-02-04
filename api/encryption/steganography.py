from email.mime import image
from helper.stegano.LSBSteg import *
from helper.encryption.transposition import encryptMessage, decryptMessage


#encoding

def encoding(image, msg):
    steg = LSBSteg(cv2.imread(image))
    cipher = encryptMessage(msg)
    img_encoded = steg.encode_text(cipher)
    cv2.imwrite("./encrytped/my_new_image.png", img_encoded)


def decoding():
    im = cv2.imread("./encrytped/my_new_image.png")
    steg = LSBSteg(im)
    text_value = steg.decode_text()
    decrypted_text = decryptMessage(text_value)
    print("TEXT VALUE:", decrypted_text)



encoding()
print("IMAGE ENCODED")
decoding()
print("IMAGE DECODED")