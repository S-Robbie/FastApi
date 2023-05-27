from pydantic import BaseModel, EmailStr
from typing import List, Optional
from models.events import Event
from sqlmodel import JSON, SQLModel, Field, Column

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr
    password: str
    username: str
    events: Optional[List[Event]] = Field(sa_column=Column(JSON))

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "email": "robin.s@hpe.com",
                "username": "srob",
                "events": [
                    {
                        "title": "FastAPI Book Launch",
                        "image": "https:linktomyimage.com/image.png",
                        "description": "We will be discussing the contents of the FastAPI book in this event. \\"
                                       "Ensure to come with your own copy to win gifts!",
                        "tags": ["python", "fastapi", "book", "launch"],
                        "location": "Google Meet"
                    }
                ]
            }
        }


class UserSignIn(SQLModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
        "example": {
                "email": "fastapi@packt.com",
                "password": "strong!!!",
                "events": []
            }
        }

class TokenResponse(BaseModel):
    access_token: str
    token_type: str