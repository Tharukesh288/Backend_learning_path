from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")        # Secret key used to sign the JWT
ALGORITHM = os.getenv("ALGORITHM")          # Algorithm used to sign the JWT

