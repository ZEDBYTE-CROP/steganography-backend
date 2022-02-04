from starlette.endpoints import HTTPEndpoint
from api import APIResponse

from pydantic import ValidationError

from model.query import encryption_query
from model.encryption import textdecryptModel
from helper.encryption.transposition import decryptMessage
from utils import ErrorFormatter


class TextDecryptionAPI(HTTPEndpoint):
    async def post(self, request):
        try:
            request_body = await request.json()
            stage1Encryption = textdecryptModel(**request_body)
            db_client = request['app'].state.DB_CLIENT
            encrypted_text = await encryption_query.get_cipher(db_client, stage1Encryption)
            cipher = decryptMessage(encrypted_text)
            
            return APIResponse( status = "OK", message = "text encrypted")
            
                

        except ValidationError as e:
            errors = ErrorFormatter(e.errors()).formatted_errors
            errors = {"errors":errors[0]}
            return APIResponse(status = "ERROR", message = errors["errors"]["message"], error=errors["errors"]["type"], status_code = 200)

