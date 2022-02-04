from unittest import result
from starlette.endpoints import HTTPEndpoint
from api import APIResponse

from pydantic import ValidationError

from model.query import encryption_query
from model.encryption import transpositionModel
from helper.encryption.transposition import encryptMessage
from helper.generateRandom import ran_gen
from utils import ErrorFormatter


class TextEncryptionAPI(HTTPEndpoint):
    async def post(self, request):
        try:
            request_body = await request.json()
            stage1Encryption = transpositionModel(**request_body)
            db_client = request['app'].state.DB_CLIENT
            cipher = encryptMessage(stage1Encryption.original_text)
            randomPostId = ran_gen(5, "1234567890")
            await encryption_query.update_cipher(db_client, cipher, randomPostId, stage1Encryption)
            return APIResponse( status = "OK", message = "text encrypted", result = {"cipher":cipher,"randomPostId" : randomPostId})
            
                

        except ValidationError as e:
            errors = ErrorFormatter(e.errors()).formatted_errors
            errors = {"errors":errors[0]}
            return APIResponse(status = "ERROR", message = errors["errors"]["message"], error=errors["errors"]["type"], status_code = 200)

