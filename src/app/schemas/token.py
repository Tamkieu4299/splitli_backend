from typing import Optional, Union

from pydantic import UUID4, BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Union[str, None] = None

class TokenVendorData(BaseModel):
    user_id: Union[str, None] = None

