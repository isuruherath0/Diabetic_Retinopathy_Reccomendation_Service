import os
from dotenv import load_dotenv
load_dotenv("config/.env")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("REGION_NAME")
MONGODB_URI = os.getenv("MONGODB_URI")

