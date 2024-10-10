import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
import io, os, bcrypt
from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import requests

# il faudrait un chatbot avec l'onglet aide, et un chat bot qui pose des questions et redirige vers un interlocuteur en ligne en direct
# https://www.twilio.com/en-us/whatsapp/pricing

load_dotenv('.env.local')

app = Flask(__name__)
CORS(app)

# Configurations sécurisées
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret')

jwt = JWTManager(app)

config = {
    'user': os.getenv('DB_USER', 'default_user'),
    'password': os.getenv('DB_PASSWORD', 'default_password'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'default_db_name'),
    'raise_on_warnings': True,
    'port': int(os.getenv('DB_PORT', 3306))
}

def query_db(query, args=(), one=False):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(query, args)
    rv = cursor.fetchall()
    cursor.close()
    cnx.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the home page!"})

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = query_db("SELECT * FROM users WHERE username=%s", (username,), one=True)

    if user:
        print(f"User found: {user}")  # Débogage : vérifier l'utilisateur trouvé

        # Vérifier si le mot de passe correspond
        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            access_token = create_access_token(identity=username)
            print(f"Access token created: {access_token}")  # Débogage : vérifier la création du token
            return jsonify(access_token=access_token)
        else:
            print("Password does not match")  # Débogage : mot de passe incorrect
            return jsonify({"error": "Palavra passe incorrecta."}), 401
    else:
        print("User not found")  # Débogage : utilisateur non trouvé
        return jsonify({"error": "nome de utilizador incorrecto"}), 401

import requests

@app.route('/chat', methods=['POST'])
def chat():
    message = request.json.get('message', None)
    if not message:
        return jsonify({"error": "Message not provided"}), 400

    # Envoyer le message à Wit.ai
    access_token = os.getenv('WIT_AI_ACCESS_TOKEN')

    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(f'https://api.wit.ai/message?v=20240823&q={message}', headers=headers)
    data = response.json()

    # Détecter l'intention
    intent = data.get('intents', [{}])[0].get('name')

    # Réponse basée sur l'intention
    if intent == 'greet':
        reply = "Bom dia! Como posso ajudar?"
    else:
        # Si l'intention est inconnue, on l'enregistre dans la base de données
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        
        # Vérifier si l'intent existe déjà dans la table
        existing_intent = query_db("SELECT * FROM intent WHERE nom=%s", (intent,), one=True)
        if not existing_intent:
            cursor.execute("INSERT INTO intent (nom, response, unknown) VALUES (%s, %s, %s)",
                           (intent, None, True))
            cnx.commit()

        cursor.close()
        cnx.close()

        reply = "Desculpe, não entendi."

    return jsonify({"response": reply})


    
@app.route('/register', methods=['POST'])
def signup():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Vérifier si l'utilisateur existe déjà
    existing_user = query_db("SELECT * FROM users WHERE username=%s", (username,), one=True)
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    # Hasher le mot de passe
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insérer le nouvel utilisateur dans la base de données
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    cnx.commit()
    cursor.close()
    cnx.close()

    return jsonify({"message": "User created successfully"}), 201

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({"message": "You are viewing a protected route!"})

@app.errorhandler(404)
def page_not_found(e):
    # Rediriger vers une page d'erreur 404 personnalisée
    return redirect(url_for('error_404'))

@app.route('/error404')
def error_404():
    return jsonify({"error": "Page not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
