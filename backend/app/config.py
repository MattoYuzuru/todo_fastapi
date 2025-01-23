import os

from dotenv import load_dotenv
import pytz

load_dotenv()


DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30
TIME_ZONE = pytz.timezone("Europe/Moscow")
