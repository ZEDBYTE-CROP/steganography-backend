import boto3
from botocore.exceptions import ClientError
import io

DEFAULT_BUCKET = "steganography"
DEFAULT_REGION = "ap-south-1"


class S3Manager():
    """A manager to handle s3 buckets and file transfers"""

    def __init__(self, service='s3', region=DEFAULT_REGION, access_key_id="AKIAV7EZJONVDBVF7H6G", secret_access_key="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"):
        #self.base_url = BASE_URL
        try:
           if  not (access_key_id and access_key_id):
               raise RuntimeError("Access tokens not specified")
        except KeyError:
            raise RuntimeError("aws resource not specified in the configuration")

        self.access_key_id = access_key_id 
        self.secret_access_key = secret_access_key
        self.default_bucket = DEFAULT_BUCKET
        self.default_region = DEFAULT_REGION
        self._service = service
        self.s3 = boto3.client(self._service,
                               aws_access_key_id=self.access_key_id,
                               aws_secret_access_key=self.secret_access_key)

    def createBucket(self, bucket_name, region=None):
        """create a s3 bucket in a given region"""
        try:
            if region is None:
                self.s3.create_bucket(Bucket=bucket_name)
            else:
                location = {'LocationConstraint': region}
                self.s3.create_bucket(Bucket=bucket_name,
                                      CreateBucketConfiguration=location)
        except ClientError as e:
            print("Bucket Creation Failed!!, Error:", e)
            return False
        return True

    def listBuckets(self):
        return self.s3.list_buckets()

    def uploadFile(self, filename, bucket=None, object_name=None, extra_args=None):
        """uploads file to specified bucket in s3"""
        bucket = bucket or self.default_bucket
        if object_name is None:
            object_name = filename

        try:
            response = self.s3.upload_fileobj(
                filename, bucket, object_name, ExtraArgs=extra_args)
        except ClientError as e:
            print(e)
            return False
        return response

    def deleteFile(self, bucket=None, object_name=None):
        """uploads file to specified bucket in s3"""
        bucket = bucket or self.default_bucket
        try:
            response = self.s3.delete_objects(Bucket = bucket, Delete = {"Objects" : [{"Key" : object_name}]})
        except ClientError as e:
            print(e)
            return False
        return response

    def downloadFile(self, bucket, object_name, filename):
        try:
            self.s3.download_file(bucket, object_name, filename)
        except:
            print("Error occured while downloading file")

    def getBucketPolicy(self, bucket=None):
        if bucket is None:
            raise ValueError("Bucket name shouldn't be None")
        bucket_policy = self.s3.get_bucket_policy(bucket=bucket)
        return bucket_policy['Policy']

    # def setBucketPolicy(self, bucket=None, policy=None):
    #     if bucket is None:
    #         raise ValueError("Bucket name shouldn't be None")
    #     if policy is None:
    #         raise ValueError("Policy shouldn't be None")
    #     s3.put_bucket_policy(Bucket=bucket, Policy=policy)

    def deleteBucket(self, bucket):
        pass

    def verifyPolicy(self, policy):
        pass
