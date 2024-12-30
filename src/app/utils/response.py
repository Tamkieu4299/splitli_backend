from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def convert_response(status: bool, message: str, data: any):
    response = {"status": status, "message": message, "data": data}
    return response

class Response(JSONResponse):
    def __init__(
        self, 
        content = None, 
        status_code: int = 200, 
        message: str = None,
        headers: dict = None, 
        media_type: str = None
    ):
        custom_content = {
            "status": "success" if status_code == 200 else "error",
            "data": jsonable_encoder(content),
            "message": message
        }
        super().__init__(content=jsonable_encoder(custom_content), status_code=status_code, headers=headers, media_type=media_type)
