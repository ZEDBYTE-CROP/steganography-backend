from aws.aws_s3_handler import S3Manager
from datetime import datetime

DEFAULT_BUCKET = "steganography"
DEFAULT_REGION = "ap-south-1"
STORAGE_URL = "https://{}.s3.{}.amazonaws.com/{}/{}"

class ImageUploader():

    def __init__(self):
        self.BASE_URL = STORAGE_URL


    def uploadImages(self, images, folder, extra_args=None, bucket=DEFAULT_BUCKET, file_type=None):
            url : str 

            filename = str(datetime.now())+".mp4" if file_type == "video/mp4" else str(datetime.now())+".jpg"
            
            try:
                S3Manager().uploadFile(
                    images, bucket, object_name = "{}/{}".format(folder,filename), extra_args=extra_args)
                url = self.constructImageURL(
                    bucket, DEFAULT_REGION, folder, filename)
                return url

            except Exception as e:
                print(e)
            
    

    def constructImageURL(self, bucket, region, folder, key):
        """constructs URl object's url"""
        return self.BASE_URL.format(bucket, region, folder, key)

class ImageRemover():

    def __init__(self):
        self.BASE_URL = STORAGE_URL


    def deleteImages(self, folder, bucket=DEFAULT_BUCKET):
            try:
                S3Manager().deleteFile(
                    bucket, object_name = folder)
            except Exception as e:
                print(e)


class ImageUpdater():

    def __init__(self):
        self.BASE_URL = STORAGE_URL


    def updateImages(self, images, folder, extra_args=None, bucket=DEFAULT_BUCKET, file_type=None):
        url : str 
        filename = str(datetime.now())+".mp4" if file_type == "video/mp4" else str(datetime.now())+".jpg"
        try:
            S3Manager().deleteFile(bucket, object_name = folder)
            S3Manager().uploadFile(images, bucket, object_name = "{}/{}".format(folder,filename), extra_args=extra_args) 
            url = self.constructImageURL(bucket, DEFAULT_REGION, folder, filename)
        except Exception as e:
            print(e)
        return url

    def constructImageURL(self, bucket, region, folder, key):
        """constructs URl object's url"""
        return self.BASE_URL.format(bucket, region, folder, key)



