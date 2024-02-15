from pydantic import BaseModel

class WatchlistUserBase(BaseModel):
    username: str
    email: str

class UserCreate(WatchlistUserBase):
    password: str

class User(WatchlistUserBase):
    id: int

    class ConfigDict:
        from_attributes = True
        validate_assignment = True