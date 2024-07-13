from pydantic import BaseModel
from typing import Optional, List


class UserSchema(BaseModel):
    id: int
    name: str
    email: str


class AddressSchema(BaseModel):
    """ Define how an address should be represented
    """
    id: int
    zip_code: str
    street: str
    complement: Optional[str] = None
    neighborhood: Optional[str] = None
    city: str
    state: str
    ibge_code: Optional[int] = None
    gia_code: Optional[int] = None
    ddd_code: Optional[int] = None
    siafi_code: Optional[int] = None
    created_at: str
    updated_at: str
    user: UserSchema


class AddessGetQuerySchema(BaseModel):
    """ Define the structure that represents the query string of a get address request.
    """
    zip_code: int
    user_id: int


class AddessUpdateQuerySchema(BaseModel):
    """ Define the structure that represents the query string of a get address request.
    """
    address_id: int
    zip_code: int
