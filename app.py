import asyncio
import secrets
from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for, session
import certifi
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer, util
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Remplacez les valeurs suivantes par vos informations MongoDB Atlas
MONGO_URI = "mongodb+srv://zahirikram09:if6tTu7zYm5LxJ4i@forsati.sgoglff.mongodb.net/"

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())

db = client['Advisor']
users_collection = db['User']
jobs_collection = db['Job']
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/inscription', methods=['GET', 'POST'])
def inscription1():
    if request.method == 'POST':
        # Logique pour gérer l'inscription
        return redirect(url_for('home'))
    return render_template('inscription1.html')

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        # Logique pour gérer la connexion
        return redirect(url_for('home'))
    return render_template('connexion.html')

@app.route('/recruteur_employee')
def recruteur_employee():
    return render_template('recruteur_employee.html')

@app.route('/recruteur')
def lien_vers_recruteur():
    return render_template('lien_vers_recruteur.html')
# Ajouter d'autres routes si nécessaire

@app.route('/submitConnection', methods=['POST'])
def submitConnection():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Chercher l'utilisateur dans la base de données
        user = users_collection.find_one({'email': email, 'password': password})
        
        if user:
             session['user_id'] = str(user['_id'])
             session['email'] = user['email']
             return redirect(url_for('employee'))
        else:
            # Si l'utilisateur n'existe pas
            return "Utilisateur non trouvé", 401

    return redirect(url_for('connexion'))

@app.route('/employee')
def employee():
    if 'user_id' in session:
        user_id = session['user_id']
        # Récupérer les informations de l'utilisateur en utilisant son ID
        user = users_collection.find_one({'_id': ObjectId(user_id)})

        if user:
            # Récupérer les compétences de l'utilisateur
            user_skills = user.get('competences', [])
            similar_job_ids = asyncio.run(get_similar_jobs(user_skills=user_skills))

            # Récupérer les informations complètes des offres d'emploi en utilisant les IDs
            similar_offers = list(jobs_collection.find({'_id': {'$in': similar_job_ids}}))

            # Convertir les ObjectId en chaînes de caractères pour les utiliser dans le template
            for offer in similar_offers:
                offer['_id'] = str(offer['_id'])

            return render_template('employee.html', user=user, similar_offers=similar_offers)
        else:
            return redirect(url_for('connexion'))
    else:
        return redirect(url_for('connexion'))

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
if __name__ == '__main__':

    app.run(debug=True)
