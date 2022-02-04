from unittest import result
from starlette.endpoints import HTTPEndpoint
from api import APIResponse

from pydantic import ValidationError

from model.query import encryption_query
from model.encryption import verifyModel
from helper.encryption.transposition import encryptMessage
from helper.generateRandom import ran_gen
from utils import ErrorFormatter


class VerifyOTPAPI(HTTPEndpoint):
    async def post(self, request):
        try:
            request_body = await request.json()
            details = verifyModel(**request_body)
            db_client = request['app'].state.DB_CLIENT
            original_otp = details.otp
            stringArray = original_otp.split("-")
            user_id = stringArray[0]
            encrypted_id = stringArray[1]
            otp = stringArray[2]
            devrypted_details = await encryption_query.verifyOTP(db_client, user_id, encrypted_id )
            return APIResponse( status = "OK", message = "text encrypted", result = devrypted_details)
            
                

        except ValidationError as e:
            errors = ErrorFormatter(e.errors()).formatted_errors
            errors = {"errors":errors[0]}
            return APIResponse(status = "ERROR", message = errors["errors"]["message"], error=errors["errors"]["type"], status_code = 200)

