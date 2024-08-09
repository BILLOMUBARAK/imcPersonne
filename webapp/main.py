from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Float

import json

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:groupe7@db/imcpersonne'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class imcTable(db.Model):
    __tablename__ = 'imcTable'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    taille = db.Column(db.Integer)
    poids = db.Column(db.Integer)
    imc = db.Column(db.Float)  # Utilisation de db.Float pour déclarer un type de colonne flottant
    interpretation = db.Column(db.String(100))

    def __init__(self, nom, prenom, taille, poids, imc, interpretation):
        self.nom = nom
        self.prenom = prenom
        self.taille = taille
        self.poids = poids
        self.imc = imc
        self.interpretation = interpretation

@app.route('/')
def index():
    return render_template('formulaireQuestion.html')

@app.route('/submit', methods=['POST'])
def submit():
    nom = request.form['nom']
    prenom = request.form['prenom']
    taille = int(request.form['taille'])
    poids = int(request.form['poids'])

    # Validation des valeurs de taille et de poids
    if taille <= 0 or poids <= 0:
        return "La taille et le poids doivent être des valeurs positives.", 400

    imc = calcul_imc(poids, taille)
    interpretation = interprete_imc(imc)

    # Afficher les données dans la console
    print(f"nom: {nom}")
    print(f"prenom: {prenom}")
    print(f"taille: {taille}")
    print(f"poids: {poids}")

    # Créer une instance de la classe de modèle imc et l'ajouter à la session
    new_imc = imcTable(nom=nom, prenom=prenom, taille=taille, poids=poids, imc=imc, interpretation=interpretation)
    db.session.add(new_imc)
    db.session.commit()

    # Récupérer toutes les données de la base de données et les retourner en tant que réponse
    users = imcTable.query.all()
    users_list = []
    for user in users:
        user_data = {
            'id': user.id,
            'nom': user.nom,
            'prenom': user.prenom,
            'taille': user.taille,
            'poids': user.poids,
            'imc': user.imc,
            'interpretation': user.interpretation
        }
        users_list.append(user_data)

    return jsonify(users_list)

def calcul_imc(poids, taille_cm):
    if taille_cm <= 0 or poids <= 0:
        raise ValueError("La taille et le poids doivent être des valeurs positives.")
    taille_m = taille_cm / 100  # Conversion de cm en mètres
    imc = poids / (taille_m ** 2)
    return imc

def interprete_imc(imc):
    if imc < 18.5:
        return "Insuffisance pondérale"
    elif imc < 25:
        return "Corpulence normale"
    elif imc < 30:
        return "Surpoids"
    else:
        return "Obésité"

if __name__ == '__main__':
    with app.app_context():
        # Créer toutes les tables définies dans les modèles SQLAlchemy
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
