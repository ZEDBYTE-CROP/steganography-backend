from pyparsing import Opt
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import uvicorn
from config import config

# user imports
from api.users.signup import SignUpAPI
from api.users.login import LogInAPI
# text encryption
from api.encryption.textEncryption import TextEncryptionAPI
# image encryption
from api.encryption.imageEncrypt import ImageEncryptionAPI
# send otp
from api.messages.sendOtp import SendOtpAPI
# generate qr
from api.encryption.generateQR import ImageQRcodeAPI
# verifyOTP
from api.encryption.verifyOTP import VerifyOTPAPI
# share
from api.users.shareQR import SendQrAPI
# list all posts
from api.users.listQr import ListQRAPI

routes = [
    Route('/signup', SignUpAPI),
    Route('/login', LogInAPI),
    Route('/sendotp', SendOtpAPI),
    Route('/textencryption', TextEncryptionAPI),
    Route('/imageencryption', ImageEncryptionAPI),
    Route('/imageqrcode', ImageQRcodeAPI),
    Route('/verifyOTP', VerifyOTPAPI),
    Route('/share', SendQrAPI),
    Route('/list', ListQRAPI)
    ]
    
middleware = [
    Middleware(CORSMiddleware, allow_credentials=True, allow_origins=['*'], allow_methods=["*"],
    allow_headers=["*"])
]

app = Starlette(routes = routes, middleware=middleware)


@app.on_event("startup")
async def connection_setup():
    
    MONGODB_URL = config["mongo_db_testing"]["uri"]
    client = AsyncIOMotorClient(MONGODB_URL)
    app.state.DB_CLIENT = client


uvicorn.run(app, host="0.0.0.0", port=5000)