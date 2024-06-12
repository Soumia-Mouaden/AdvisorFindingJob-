<<<<<<< HEAD
import asyncio
import secrets
from bson import ObjectId
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import certifi
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer, util
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os
from datetime import datetime
=======
from flask import Flask, render_template, request, redirect, url_for
import os
import google.generativeai as genai
>>>>>>> b6785c78cc6dee24f25921c80b4e81e30eb3ce52

app = Flask(__name__)

# Set your API key for Google Generative AI
os.environ["GEMINI_API_KEY"] = "AIzaSyBoqdqzlcO3gt6xs2QKpxpXJTturgZvCb4"

# Configure the Generative AI model
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

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

<<<<<<< HEAD
@app.route('/submitInscription', methods=['POST'])
def submitInscription():
    # Récupérez les données du formulaire d'inscription
    lastName = request.form.get('lastName')
    firstName = request.form.get('firstName')
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')
    address = request.form.get('address')
    gender = request.form.get('gender')
    birth_date = datetime(year=int(request.form['birthYear']), 
                          month=int(request.form['birthMonth']), 
                          day=int(request.form['birthDay']))
    educationLevel = request.form.get('educationLevel')
    # keywordInputDiplome = request.form.get('keywordInputDiplome')
    diplomes_str = request.form.get('keywordInputDiplome')
    diplomes = [diplome.strip() for diplome in diplomes_str.split(',') if diplome.strip()]
    
    # languages = request.form.get('languages')
    competencies_str = request.form.get('keywordInputCompetence')
    competencies = [competence.strip() for competence in competencies_str.split(',') if competence.strip()]
    
    jobTitle = request.form.get('jobTitle')
    salaryRangeInput = request.form.get('salaryRangeInput')
    contractTypeInput = request.form.get('contractTypeInput')
    workHoursInput = request.form.get('workHoursInput')
    mobilityInput = request.form.get('mobilityInput')
    professionalExperience = request.form.get('professionalExperience')

    poste_recherche = {
        'poste': jobTitle,
        'salaire_min': salaryRangeInput,
        'type_contrat': contractTypeInput,
        'horaire': workHoursInput,
        'mobilite': mobilityInput,
        'nb_annees_experience': professionalExperience
    }

    # Insérez les données dans MongoDB
    data = {
        'nom': lastName,
        'prenom': firstName,
        'email': email,
        'tele': phone,
        'adresse': address,
        'genre': gender,
        'date_naissance': birth_date,
        'niveau_etude': educationLevel,
        'diplomes_obtenus': diplomes,
        # 'langues': langues,
        'competences': competencies,
        'poste_recherche': poste_recherche,
        'password': password
    }

    users_collection.insert_one(data)
    session['user_id'] = str(data['_id'])
    session['email'] = data['email']
    return redirect(url_for('employee'))

@app.route('/submitConnection', methods=['POST'])
def submitConnection():
=======
@app.route('/predict', methods=['POST'])
def predict():
>>>>>>> b6785c78cc6dee24f25921c80b4e81e30eb3ce52
    if request.method == 'POST':
        data = request.get_json()  # Get JSON data from the request
        user_message = data.get('message', '')  # Extract user's message from the JSON

        if user_message:  # Ensure there's a user message to process
            # Start chat session
            chat_session = model.start_chat(
                history=[
                    {"role": "user", "parts": [user_message]},
                ]
            )

            # Generate response by sending user's message
            response = chat_session.send_message(user_message)

            # Extract the generated response
            response_text = response.text.strip()

            # Return the response in text/plain format
            return response_text
        else:
            return "No message received", 400

<<<<<<< HEAD
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

@app.route('/update_poste_recherche', methods=['POST'])
def update_poste_recherche():
    data = request.json
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({"error": "User not logged in"}), 403

    poste_recherche = {
        "poste": data['poste'],
        "salaire_min": data['salaire_min'],
        "type_contrat": data['type_contrat'],
        "horaire": data['horaire'],
        "mobilite": data['mobilite'],
        "nb_annees_experience": data.get('nb_annees_experience', 0)
    }
    competences = data['competences']

    result = users_collection.update_one(
        {'_id': ObjectId(user_id)},
        {
            '$set': {
                'poste_recherche': poste_recherche,
                'competences': competences
            }
        }
    )

    if result.matched_count == 1:
        return redirect(url_for('employee'))
    else:
        return jsonify({"error": "User not found"}), 404
=======
>>>>>>> b6785c78cc6dee24f25921c80b4e81e30eb3ce52
if __name__ == '__main__':
    app.run(debug=True)
