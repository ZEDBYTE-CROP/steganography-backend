from datetime import date
from typing import List,Any
from pydantic import BaseModel


class UserModel(BaseModel):
    name:str
    phone:str
    userid:str
    password:str


class LoginModel(BaseModel):
    userid:str
    password:str

class ShareModel(BaseModel):
    peeruserid:str
    encryptionId:str
    


