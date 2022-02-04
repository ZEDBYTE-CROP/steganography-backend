
from sqlite3 import Cursor
from bson.objectid import ObjectId
from config import config


DEFAULT_DATABASE = "core"
database = config["mongo_db_testing"]["database"]
user_collection = config["mongo_db_testing"]["user_collection"]
encryption_collection = config["mongo_db_testing"]["encryption_collection"]



def convert_bson_str(doc):
    try:
        doc['_id'] = str(doc['_id'])
        return doc
    except:
        return doc


class user_query():

    async def create_new_account(db_client, user):
        db = db_client[database]
        account_details = {
            "name": user.name,
            "phone": user.phone,
            "userid": user.userid,
            "password": user.password,
            "encryptionId" : []
        }
        result = await db[user_collection].insert_one(account_details)
        return result

    async def match_credential_and_password(db_client, user):
        db = db_client[database]
        query = {"$and": [{"userid": user.userid},
                          {"password": user.password}]}
        result = await db[user_collection].find_one(query)
        return result

    async def match_user_id(db_client, user):
        db = db_client[database]
        query = {"userid": user.userid}
        result = await db[user_collection].find_one(query)
        convert_bson_str(result)
        return result

    async def share(db_client, user):
        db = db_client[database]
        query = {"userid": user.peeruserid}
        value = {"$push" : {
            "encryptionId" : user.encryptionId
        }}
        result = await db[user_collection].update_one(query,value)
        convert_bson_str(result)
        return result

    async def count(db_client):
        db = db_client[database]
        cursor = db[user_collection].find()
        number_of_documents_in_collection = await cursor.to_list(length=None)
        return len(number_of_documents_in_collection)

    async def list_of_ids(db_client, user):
        db = db_client[database]
        query = {"userid": user.userid}
        result = await db[user_collection].find_one(query)
        convert_bson_str(result)
        return result

class encryption_query():

    async def update_cipher(db_client, cipher, randomPostId, stage1Encryption):
        db = db_client[database]
        details = {
            "userId": stage1Encryption.userid,
            "encryptionId": randomPostId,
            "originalText": stage1Encryption.original_text,
            "encryptedText": cipher,
            "originalImage": "",
            "encryptedImage": "",
            "qrCode": ""
        }
        result = await db[encryption_collection].insert_one(details)
        return result

    async def update_image(db_client, originalimage, encryptedimage, stage2Encryption):
        db = db_client[database]
        query = {"$and" : [{"userId" : stage2Encryption.userid},{"encryptionId": stage2Encryption.encryptionId}]}
        details = {
            "$set" : {
            "originalImage": originalimage,
            "encryptedImage": encryptedimage,
            "qrCode": ""
            }
        }
        result = await db[encryption_collection].update_one(query,details)
        return result

    async def update_QRimage(db_client, QRcode_image, stage2Encryption):
        db = db_client[database]
        query = {"$and" : [{"userId" : stage2Encryption.userid},{"encryptionId": stage2Encryption.encryptionId}]}
        details = {
            "$set" : {
            "qrCode": QRcode_image
            }
        }
        result = await db[encryption_collection].update_one(query,details)
        return result

    async def match_user_id(db_client, user):
        db = db_client[database]
        query = {"$and" : [{"userId": user.userid},{"encryptionId": user.encryptionId}]}
        result = await db[encryption_collection].find_one(query)
        convert_bson_str(result)
        return result

    async def find_all_posts(db_client, user):
        db = db_client[database]
        query = {"encryptionId": {"$in" : user }}
        cursor = db[encryption_collection].find(query,["qrCode"])
        result = await cursor.to_list(length=None)
        return result

    async def verifyOTP(db_client, userid, encryptionId):
        db = db_client[database]
        query = {"$and" : [{"userId": userid},{"encryptionId": encryptionId}]}
        result = await db[encryption_collection].find_one(query)
        convert_bson_str(result)
        return result

    async def get_cipher(db_client, stage1Encryption):
        db = db_client[database]
        query = {"userId": stage1Encryption.userid}
        result = await db[encryption_collection].find_one(query)
        return result


    async def get_original_message(db_client, stage2Encryption):
        db = db_client[database]
        query = {"userId": stage2Encryption.userid}
        value = {"$set" : {""}}
        result = await db[encryption_collection].update_one(query)
        return result