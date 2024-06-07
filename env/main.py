from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import asyncio

# Charger les variables d'environnement
load_dotenv()

class Item(Document):
    name: str
    description: str

async def init():
    connection_string = os.getenv("MONGO_CONNECTION_STRING")
    database_name = os.getenv("MONGO_DATABASE_NAME")
    if not connection_string or not database_name:
        raise ValueError("MONGO_CONNECTION_STRING ou MONGO_DATABASE_NAME n'est pas défini dans le fichier .env")

    client = AsyncIOMotorClient(connection_string, tls=True, tlsAllowInvalidCertificates=True)
    database = client[database_name]
    await init_beanie(database, document_models=[Item])
    print("Connexion réussie à MongoDB!")

async def main():
    await init()
    print("debut")

    # Ajouter le premier élément
    item1 = Item(name="First Item", description="This is the first sample item")
    await item1.insert()
    print("First Item inserted!")

    # Ajouter le second élément
    item2 = Item(name="Second Item", description="This is the second sample item")
    await item2.insert()
    print("Second Item inserted!")

if __name__ == "__main__":
    asyncio.run(main())
