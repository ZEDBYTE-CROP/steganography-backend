from starlette.endpoints import HTTPEndpoint
from api import APIResponse

from pydantic import ValidationError

from model.query import user_query
from model.user import LoginModel
from utils import ErrorFormatter


class LogInAPI(HTTPEndpoint):
    async def post(self, request):
        try:
            request_body = await request.json()
            user = LoginModel(**request_body)
            db_client = request['app'].state.DB_CLIENT

            match_credentials = await user_query.match_credential_and_password(db_client, user)
            if match_credentials:
                return APIResponse( status = "OK", message = "loggedin successfully", result = {"userid" : match_credentials["userid"]})
            else:
                return APIResponse( status = "ERROR", message = "invalid userid or password", status_code = 200 )
                

        except ValidationError as e:
            errors = ErrorFormatter(e.errors()).formatted_errors
            errors = {"errors":errors[0]}
            return APIResponse(status = "ERROR", message = errors["errors"]["message"], error=errors["errors"]["type"], status_code = 200)

