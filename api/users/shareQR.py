from starlette.endpoints import HTTPEndpoint
from api import APIResponse

from pydantic import ValidationError

from model.query import user_query
from model.user import ShareModel
from utils import ErrorFormatter


class SendQrAPI(HTTPEndpoint):
    async def post(self, request):
        try:
            request_body = await request.json()
            userDetails = ShareModel(**request_body)
            db_client = request['app'].state.DB_CLIENT

            updated = await user_query.share(db_client, userDetails)
            if updated:
                return APIResponse( status = "OK", message = "success")
            else:
                return APIResponse( status = "ERROR", message = "fail")

        except ValidationError as e:
            errors = ErrorFormatter(e.errors()).formatted_errors
            errors = {"errors":errors[0]}
            return APIResponse(status = "ERROR", message = errors["errors"]["message"], error=errors["errors"]["type"], status_code = 200)

