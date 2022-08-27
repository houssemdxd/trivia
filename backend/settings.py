from dotenv import load_dotenv
import os
load_dotenv()
DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
DB_NAME = os.environ.get("DB_NAME")
DB_USER=os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
