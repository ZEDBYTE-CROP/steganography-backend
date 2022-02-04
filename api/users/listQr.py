from starlette.endpoints import HTTPEndpoint
from api import APIResponse

from pydantic import ValidationError

from model.query import user_query, encryption_query
from model.encryption import textdecryptModel
from utils import ErrorFormatter
import json
from bson import json_util

class ListQRAPI(HTTPEndpoint):
    async def post(self, request):
        try:
            request_body = await request.json()
            userDetails = textdecryptModel(**request_body)
            db_client = request['app'].state.DB_CLIENT

            user = await user_query.list_of_ids(db_client, userDetails)
            list_of_posts = await encryption_query.find_all_posts(db_client, user["encryptionId"])
            return APIResponse( status = "OK", message = "success", result = json.loads(json_util.dumps(list_of_posts)))
                

        except ValidationError as e:
            errors = ErrorFormatter(e.errors()).formatted_errors
            errors = {"errors":errors[0]}
            return APIResponse(status = "ERROR", message = errors["errors"]["message"], error=errors["errors"]["type"], status_code = 200)

