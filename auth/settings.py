import os

from dotenv import load_dotenv
from typing import Optional
from pydantic import BaseSettings

load_dotenv()
class Settings(BaseSettings):
    SECRET_KEY: Optional[str] =  os.getenv('SECRET_KEY')

    # def __init__(self):
    #     load_dotenv()
    #     self.SECRET_KEY = os.getenv('SECRET_KEY')