from unittest import result
from starlette.endpoints import HTTPEndpoint
from api import APIResponse
from helper.ImageHandler import ImageUploader

from pydantic import ValidationError
import qrcode

import math, random
from model.query import encryption_query, user_query
from model.encryption import QRModel
from utils import ErrorFormatter
from helper.encryption.transposition import encryptMessage

def generateOTP() :
 
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = ""
    length = len(string)
    for i in range(6) :
        OTP += string[math.floor(random.random() * length)]
 
    return OTP

def upload(images, user_id):
        """uploads Images to the cloud"""

        UPLOAD_ARGS = {'ContentDisposition': "inline",
                       'ContentType': 'image/jpeg'}
        if images:
            try:
                url = ImageUploader().uploadImages(images, folder = "{}".format(user_id), extra_args=UPLOAD_ARGS)
                return url
            except Exception as e:
                raise e
        return []

def generateQR_link(userdetails):
    url = "http://0f15-122-174-17-86.ngrok.io"
    body = "{}-{}-{}".format(userdetails['userId'],userdetails['encryptionId'],generateOTP())
    QR_URL = "{}/sendotp?body={}".format(url,body)
    print(QR_URL)
    return QR_URL

class ImageQRcodeAPI(HTTPEndpoint):

    async def post(self, request):
        try:
            request_body = await request.json()
            user = QRModel(**request_body)
            db_client = request['app'].state.DB_CLIENT
            userdetails = await encryption_query.match_user_id(db_client, user)
            print(userdetails)
            QR_code_link = generateQR_link(userdetails)
            print(QR_code_link)
            #Generate QR Code
            img=qrcode.make(QR_code_link)
            img.save('QRcode.jpg')
            with open("QRcode.jpg","r+b") as image_file:
                QRcode_image = upload(image_file, request_body["userid"])
            await encryption_query.update_QRimage(db_client, QRcode_image, user)
            return APIResponse( status = "OK", message = "QRcode generated", result = QRcode_image)
                

        except ValidationError as e:
            errors = ErrorFormatter(e.errors()).formatted_errors
            errors = {"errors":errors[0]}
            return APIResponse(status = "ERROR", message = errors["errors"]["message"], error=errors["errors"]["type"], status_code = 200)

