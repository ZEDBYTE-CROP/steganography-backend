from starlette.endpoints import HTTPEndpoint
from api import APIResponse
from aws.aws_s3_handler import S3Manager
from helper.ImageHandler import ImageUploader


from pydantic import ValidationError

from model.query import encryption_query
from model.encryption import imageEncryptModel
from helper.stegano import LSBSteg
from helper.stegano.LSBSteg import *
from utils import ErrorFormatter
from helper.encryption.transposition import encryptMessage


def encoding(image_url, msg):
     with open("originalImage.jpg","wb") as f:
        image = image_url.split('https://steganography.s3.ap-south-1.amazonaws.com/')
        S3Manager().s3.download_fileobj('steganography', image[1], f)
        steg = LSBSteg(cv2.imread("originalImage.jpg"))
        cipher = encryptMessage(msg)
        img_encoded = steg.encode_text(cipher)
        cv2.imwrite("encryptedImage.jpg", img_encoded)
  
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

class ImageEncryptionAPI(HTTPEndpoint):

    async def post(self, request):
        try:
            request_body = await request.form()
            stage2Encryption = imageEncryptModel(**request_body)
            db_client = request['app'].state.DB_CLIENT
            originalimage = upload(request_body["originalImage"].file, request_body["userid"])
            message = await encryption_query.get_cipher(db_client, stage2Encryption)   
            encoding(originalimage, message["originalText"])
            with open("encryptedImage.jpg","r+b") as image_file:
                encrypted_image = upload(image_file, request_body["userid"])
            await encryption_query.update_image(db_client, originalimage, encrypted_image, stage2Encryption)
            return APIResponse( status = "OK", message = "image encrypted", result = encrypted_image)
            
                

        except ValidationError as e:
            errors = ErrorFormatter(e.errors()).formatted_errors
            errors = {"errors":errors[0]}
            return APIResponse(status = "ERROR", message = errors["errors"]["message"], error=errors["errors"]["type"], status_code = 200)

