import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv('USER') or ''
PASSWORD = os.getenv('PASSWORD') or ''
