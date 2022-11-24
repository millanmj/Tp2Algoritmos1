from dotenv import load_dotenv, dotenv_values
import os
from dataclasses import dataclass

@dataclass
class Settings:
    
    APIKEY: str = ''

load_dotenv()

settings = Settings(
    APIKEY=os.getenv('APIKEY'))
