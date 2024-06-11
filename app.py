from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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
