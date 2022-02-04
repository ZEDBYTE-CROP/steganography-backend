from datetime import date
from typing import List,Any
from pydantic import BaseModel, HttpUrl, validator, root_validator


class transpositionModel(BaseModel):
    userid:str
    original_text:str

class textdecryptModel(BaseModel):
    userid:str

class verifyModel(BaseModel):
    otp:str

class QRModel(BaseModel):
    userid:str
    encryptionId:str

class imageEncryptModel(BaseModel):
    userid:str = None
    encryptionId:str
    originalImage:Any

class LoginModel(BaseModel):
    userid:str
    password:str