from sentence_transformers import SentenceTransformer, util
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

# Charger le modèle
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

async def get_similar_jobs(user_skills):
    # Connexion à la base de données MongoDB
    client = AsyncIOMotorClient("mongodb+srv://zahirikram09:if6tTu7zYm5LxJ4i@forsati.sgoglff.mongodb.net/")
    db = client['Advisor']
    jobs_collection = db['Job']

    # Récupérer les offres d'emploi depuis MongoDB
    jobs = await jobs_collection.find().to_list(None)

    # Liste des phrases existantes (compétences des offres)
    list_competences = []
    job_ids = []
    for job in jobs:
        competences = job.get("Compétences", "")
        list_competences.append(competences)
        job_ids.append(job.get("_id"))

    # Concaténer les compétences dans chaque sous-liste
    sentences = ["".join(items) for items in list_competences]

    # Concaténer les compétences de l'utilisateur en une seule phrase
    input_sentence = " ".join(user_skills)

    # Encoder les phrases existantes et la phrase d'entrée
    embeddings = model.encode(sentences)
    input_embedding = model.encode([input_sentence])[0]

    # Calculer les similarités cosinus entre la phrase d'entrée et chaque phrase de la liste
    similarities = util.pytorch_cos_sim(input_embedding, embeddings)[0]

    # Trouver les indices des 10 plus grandes similarités
    top_k = 10
    top_k_indices = similarities.argsort(descending=True)[:top_k]

    # Retourner les IDs des offres les plus similaires
    similar_job_ids = [job_ids[idx] for idx in top_k_indices]

    return similar_job_ids

# Exemple d'utilisation
user_skills = ["python", "java", "data analysis"]

# Exécuter la fonction asynchrone
similar_jobs = asyncio.run(get_similar_jobs(user_skills))
print(similar_jobs)
