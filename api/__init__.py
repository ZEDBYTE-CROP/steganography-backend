from typing import Any
from starlette.responses import JSONResponse

class APIResponse(JSONResponse):
    def __init__(self, status="OK", result={}, message="", error={}, status_code=200):
        if error and status_code == "OK":
            status="UNKNOWN ERROR"
        content = {
            "status":status,
             "message":message,
             "result": result,
             "error": error,
        }
        super().__init__(content, status_code = status_code)
    