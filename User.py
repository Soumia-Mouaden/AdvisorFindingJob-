from typing import List
from datetime import date
from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
from enum import Enum
import os
import asyncio

# Load environment variables from .env file
load_dotenv()

class Gender(str, Enum):
    FEMALE = "femme"
    MALE = "homme"

class Language(BaseModel):
    langue: str
    niveau: str  # Assuming niveau is a string like "beginner", "intermediate", "advanced"

class PosteRecherche(BaseModel):
    poste: str
    salaire_min: float
    type_contrat: str  # e.g., "CDI", "CDD", "Freelance"
    horaire: str  # e.g., "Full-time", "Part-time"
    mobilite: str  # e.g., "Yes", "No"
    nb_annees_experience: int

class User(Document):
    nom: str
    prenom: str
    email: EmailStr
    tele: str
    gmail: EmailStr  # Assuming this is a separate field
    adresse: str
    genre: Gender
    date_naissance: date
    niveau_etude: str
    diplomes_obtenus: List[str]
    langues: List[Language]
    competences: List[str]
    poste_recherche: PosteRecherche
    password: str 
    similar_offer_ids: List[str] = []  # List of IDs of similar offers
     # Storing plain text password

    class Settings:
        collection = "users"  # Name of the MongoDB collection

async def init():
    connection_string = os.getenv("MONGO_CONNECTION_STRING")
    database_name = os.getenv("MONGO_DATABASE_NAME")
    client = AsyncIOMotorClient(connection_string)
    database = client[database_name]
    await init_beanie(database, document_models=[User])

async def main():
    await init()
    user = User(
        nom="Doe",
        prenom="John",
        email="john.doe@example.com",
        tele="1234567890",
        gmail="john.doe@gmail.com",
        adresse="123 Main St",
        genre=Gender.MALE,
        date_naissance=date(1990, 1, 1),
        niveau_etude="Bachelor's Degree",
        diplomes_obtenus=["Bachelor of Science"],
        langues=[Language(langue="English", niveau="Advanced")],
        competences=["Python", "Data Analysis","Oracle","Powerpoint"],
        poste_recherche=PosteRecherche(
            poste="Data Scientist",
            salaire_min=50000,
            type_contrat="Full-time",
            horaire="Day",
            mobilite="Yes",
            nb_annees_experience=3,
        ),
        password="securepassword123"  
        # Storing plain text password
    )
    await user.insert()
    print("User inserted!")

if __name__ == "__main__":
    asyncio.run(main())
