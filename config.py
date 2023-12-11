#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    TOKEN: str
    BOT_USERNAME: str

    class Config:
        env_file = os.path.join(os.getcwd(), '.env')
        env_file_encoding = 'utf-8'

settings = Settings()
