from dotenv import load_dotenv
import os

load_dotenv()

TOKEN_BOT = os.getenv("TOKEN_BOT")
ADMINS = {623621871}

if not all([TOKEN_BOT]):
    raise ValueError("You need to configure '.env' first!")
