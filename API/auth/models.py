from pydantic import BaseModel


class VerifyRequest(BaseModel):
    username: str
    password_hash: str
