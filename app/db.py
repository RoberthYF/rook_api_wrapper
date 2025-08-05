# app/db.py

import motor.motor_asyncio
from dotenv import load_dotenv
from typing import cast
import os

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB = os.getenv("MONGODB_DB")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION")

# Validación estricta para evitar valores None
if not all([MONGODB_URI, MONGODB_DB, MONGODB_COLLECTION]):
    raise ValueError("One or more MongoDB environment variables are missing.")

# Cliente asincrónico
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)

database = client[cast(str, MONGODB_DB)]
collection = database[cast(str, MONGODB_COLLECTION)]
