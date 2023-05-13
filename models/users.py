from pydantic import BaseModel, EmailStr
from typing import List, Optional
from models.events import Event

class User(BaseModel):
    id: Optional[int]
    email: EmailStr
    password: str
    username: str
    events: Optional[List[Event]]

    class Config:
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


class UserSignIn(BaseModel):
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