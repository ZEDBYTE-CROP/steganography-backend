from starlette.endpoints import HTTPEndpoint
from api import APIResponse

from pydantic import ValidationError

from model.query import user_query
from model.user import UserModel
from utils import ErrorFormatter


class SignUpAPI(HTTPEndpoint):

    async def post(self, request):
        try:
            user = await request.json()
            user = UserModel(**user)
            db_client = request['app'].state.DB_CLIENT
            total_number_of_documents = await user_query.count(db_client)
            if total_number_of_documents == 0:
                await user_query.create_new_account(db_client, user)
                return APIResponse( status = "OK", message = "signed up successfully")
            else:
                find_document_with_userId = await user_query.match_user_id(db_client, user)
                print(find_document_with_userId)
                if find_document_with_userId != None:
                    return APIResponse( status = "ERROR", message = "UserId already exits", status_code = 200 )
                else:
                    await user_query.create_new_account(db_client, user)
                    return APIResponse( status = "OK", message = "signed up successfully")
        except ValidationError as e:
            errors = ErrorFormatter(e.errors()).formatted_errors
            errors = {"errors":errors[0]}
            return APIResponse(status = "ERROR", message = errors["errors"]["message"], error=errors["errors"]["type"], status_code = 200)


