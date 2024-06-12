import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from flask import jsonify

app = Flask(__name__)

# Set your API key for Google Generative AI
os.environ["GEMINI_API_KEY"] = "AIzaSyBoqdqzlcO3gt6xs2QKpxpXJTturgZvCb4"  # Replace with your actual API key

# Configure the Generative AI model
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # No need to use the user's message
        
        response_text = "ok"

        # Return the response in JSON format
        return jsonify({'answer': response_text})
    
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


if __name__ == '__main__':
    app.run(debug=True)
