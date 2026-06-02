from pydantic import BaseModel


class VerifyRequest(BaseModel):
    username: str
    password: str
