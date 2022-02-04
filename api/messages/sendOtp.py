from starlette.endpoints import HTTPEndpoint
from api import APIResponse
from twilio.rest import Client

from pydantic import ValidationError

from model.query import user_query
from model.user import LoginModel
from utils import ErrorFormatter

images = {'post_id':"otp"}

def sendOTP(body):
    account_sid = 'AC3f8d76c8146769f6f9626a866cf13d11'
    auth_token = 'f892e358c4fa0bf19a750309803d39ba'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                                body=body,
                                from_='+17754036939',
                                to='+918825464712'
                            )
    print(message.sid)

class SendOtpAPI(HTTPEndpoint):
    async def get(self, request):
        try:
            body = request.query_params["body"]
            # print(body)
            sendOTP(body)
            return APIResponse( status = "OK", message = "message sent suc")
                 
        except ValidationError as e:
            errors = ErrorFormatter(e.errors()).formatted_errors
            errors = {"errors":errors[0]}
            return APIResponse(status = "ERROR", message = errors["errors"]["message"], error=errors["errors"]["type"], status_code = 200)

