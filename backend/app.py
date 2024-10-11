import os
import requests
from PIL import Image
from io import BytesIO
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from neo4j import GraphDatabase
from Neo4jClient import Neo4jClient

# Charger les variables d'environnement
load_dotenv('.env')

app = Flask(__name__)
CORS(app)

# Configuration pour la connexion à Neo4j
neo4j_config = {
    'uri': os.getenv('NEO4J_URI'),
    'user': os.getenv('NEO4J_USER'),
    'password': os.getenv('NEO4J_PASS')
}

# URL d'authentification MovieLens et données d'authentification
auth_url = "https://movielens.org/api/sessions"
auth_data = {
    "userName": "atf202",
    "password": "Bouboule12345"
}

# Créer une session pour gérer les cookies
session = requests.Session()

# Authentification à l'API MovieLens
response = session.post(auth_url, json=auth_data)

# Créer un driver pour la connexion à Neo4j
driver = GraphDatabase.driver(
    neo4j_config['uri'],
    auth=(neo4j_config['user'], neo4j_config['password'])
)

# Créer une instance de Neo4jClient avec le driver
neo4j_client = Neo4jClient(driver)

# Fonction pour obtenir l'image du poster d'un film
def get_poster_image(movie_id):
    if response.status_code == 200:
        # URL pour récupérer les informations sur un film
        movie_url = f"https://movielens.org/api/movies/{movie_id}"

        # Effectuer l'appel GET pour récupérer les informations du film
        movie_response = session.get(movie_url)

        if movie_response.status_code == 200:
            movie_info = movie_response.json()
            # Récupérer le chemin du poster (posterPath)
            poster_path = movie_info["data"]["movieDetails"]["movie"].get("posterPath", None)

            if poster_path:
                # Construire l'URL complète de l'image
                poster_url = f"https://image.tmdb.org/t/p/original{poster_path}"

                # Télécharger l'image
                image_response = requests.get(poster_url)
                
                # Ouvrir l'image à partir du contenu téléchargé
                img = Image.open(BytesIO(image_response.content))
                
                # Sauvegarder temporairement l'image pour l'envoyer avec Flask
                temp_image_path = "temp_poster.jpg"
                img.save(temp_image_path)

                return temp_image_path
            else:
                return None
        else:
            return None
    else:
        return None

# Route pour servir l'image du poster
@app.route('/poster/<int:movie_id>', methods=['GET'])
def get_movie_poster(movie_id):
    image_path = get_poster_image(movie_id)

    if image_path:
        return send_file(image_path, mimetype='image/jpeg')
    else:
        return jsonify({"error": "Poster not found"}), 404

# Route pour récupérer tous les films avec filtres (titre, genre, tag)
@app.route('/films', methods=['GET'])
def list_films():
    search_term = request.args.get('search_term', '')
    selected_genre = request.args.get('genres', '')
    selected_tag = request.args.get('tag', '')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 25))

    if search_term:
        films = neo4j_client.search_movies_by_title(search_term, page, page_size)
    elif selected_genre:
        films = neo4j_client.get_movies_by_genres([selected_genre], page, page_size)
    elif selected_tag:
        films = neo4j_client.get_movies_by_tag(selected_tag, page, page_size)
    else:
        films = neo4j_client.get_movies_with_tags_and_avg_rating(page, page_size)

    return jsonify(films)

# Route pour les détails d'un film spécifique avec pagination
@app.route('/filmdetails', methods=['GET'])
def film_details():
    movie_id = int(request.args.get('movie_id', 1))
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 25))

    movie_info = neo4j_client.get_movie_info(movie_id, page, page_size)

    if movie_info:
        return jsonify(movie_info)
    else:
        return jsonify({"message": "Movie not found"}), 404

# Route pour rechercher des films par titre
@app.route('/searchmovies', methods=['GET'])
def search_movies():
    search_term = request.args.get('search_term', '')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 25))

    movies = neo4j_client.search_movies_by_title(search_term, page, page_size)
    return jsonify(movies)

# Route pour récupérer les films par tag spécifique avec pagination
@app.route('/moviesbytag', methods=['GET'])
def movies_by_tag():
    tag = request.args.get('tag', '')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 25))

    movies = neo4j_client.get_movies_by_tag(tag, page, page_size)
    return jsonify(movies)

# Route pour récupérer les genres distincts
@app.route('/genres', methods=['GET'])
def get_genres():
    genres = neo4j_client.get_distinct_genres()
    return jsonify(genres)

# Route pour récupérer tous les tags distincts
@app.route('/tags', methods=['GET'])
def get_tags():
    tags = neo4j_client.get_distinct_tags()
    return jsonify(tags)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
