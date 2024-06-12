from flask import Flask, render_template, request, redirect, url_for
import os
import google.generativeai as genai

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

@app.route('/predict', methods=['POST'])
def predict():
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

if __name__ == '__main__':
    app.run(debug=True)
