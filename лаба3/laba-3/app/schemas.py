from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    client_id: str | None = None

class Client(BaseModel):
    client_id: str

class ClientInDB(Client):
    hashed_password: str
