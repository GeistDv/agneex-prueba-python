from uuid import UUID
from pydantic import BaseModel


class Token(BaseModel):
    """ Create Token
    """
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """ Token Payload
    """
    user_id: int | None = None


class Msg(BaseModel):
    """ Message
    """
    msg: str


class VerificationCreate(BaseModel):
    """ Verification CreateToken
    """
    user_id: int


class VerificationOut(BaseModel):
    """ VerificationValue
    """
    link: UUID

    class Config:
        from_attributes = True
