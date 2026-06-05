from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type:str = "bearer"
class TokenPlayload(BaseModel):
    sub: str | None = None
    exp: str | None = None
    