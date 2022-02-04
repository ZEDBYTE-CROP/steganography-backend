import qrcode
#Generate QR Code
img=qrcode.make("http://0e66-182-65-216-251.ngrok.io/sendotp")
img.save('hello.png')