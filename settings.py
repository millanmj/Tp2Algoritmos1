from dotenv import load_dotenv, dotenv_values
import os
from dataclasses import dataclass

@dataclass
class Settings:
    
    APIKEY: str = ''
    PLATE_APIKEY: str = ''
    PATH_PYS: str= ''

load_dotenv()

settings = Settings(
    APIKEY=os.getenv('APIKEY'),
    PLATE_APIKEY= os.getenv('PLATE_APIKEY'),
    PATH_PYS= os.getenv('PATH_PYS'))



