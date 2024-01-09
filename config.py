from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# App
BASE_DIR = Path(__file__).parent
SHOW_SQL_QUERY = False
APP_HOST = '127.0.0.1'
APP_PORT = 8000

# DB
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
