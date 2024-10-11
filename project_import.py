from neo4j import GraphDatabase

# Connexion à Neo4j locale
uri = "bolt://localhost:7687"  # Utilisation de l'URI locale
username = "neo4j"  # Nom d'utilisateur par défaut
password = "123456789"  # Mot de passe que tu as défini lors de l'installation

# Créer un driver Neo4j
driver = GraphDatabase.driver(uri, auth=(username, password))

# Fonction pour charger les films avec LOAD CSV (création de nœuds Movie)
def create_movies():
    with driver.session() as session:
        query = """
        LOAD CSV WITH HEADERS FROM 'file:///movies.csv' AS row
        CREATE (m:Movie {
            movieId: toInteger(row.movieId),
            title: row.title,
            genres: row.genres
        })
        """
        session.run(query)
        print("Movies created.")

# Fonction pour charger les liens IMDB et TMDB avec links.csv
def create_links():
    with driver.session() as session:
        query = """
        LOAD CSV WITH HEADERS FROM 'file:///links.csv' AS row
        MATCH (m:Movie {movieId: toInteger(row.movieId)})
        SET m.imdbId = toInteger(row.imdbId), m.tmdbId = toInteger(row.tmdbId)
        """
        session.run(query)
        print("Links loaded (IMDB and TMDB).")

# Fonction pour créer les utilisateurs avec des nœuds User
def create_users():
    with driver.session() as session:
        query = """
        LOAD CSV WITH HEADERS FROM 'file:///ratings.csv' AS row
        MERGE (u:User {userId: toInteger(row.userId)})
        """
        session.run(query)
        print("Users created.")

# Fonction pour créer les tags avec des nœuds Tag
def create_tags():
    with driver.session() as session:
        query = """
        LOAD CSV WITH HEADERS FROM 'file:///genome-tags.csv' AS row
        CREATE (:Tag {tagId: toInteger(row.tagId), tag: row.tag})
        """
        session.run(query)
        print("Tags created.")

# Fonction pour charger les relations d'évaluation avec LOAD CSV (création de relations RATED)
def create_rated_relationships():
    with driver.session() as session:
        query = """
        LOAD CSV WITH HEADERS FROM 'file:///ratings.csv' AS row
        MATCH (m:Movie {movieId: toInteger(row.movieId)})
        MATCH (u:User {userId: toInteger(row.userId)})
        CREATE (u)-[:RATED {rating: toFloat(row.rating), timestamp: toInteger(row.timestamp)}]->(m)
        """
        session.run(query)
        print("RATED relationships created.")

# Fonction pour charger les relations de tags avec LOAD CSV (création de relations TAGGED)
def create_tagged_relationships():
    with driver.session() as session:
        query = """
        LOAD CSV WITH HEADERS FROM 'file:///tags.csv' AS row
        MATCH (m:Movie {movieId: toInteger(row.movieId)})
        MATCH (u:User {userId: toInteger(row.userId)})
        CREATE (u)-[:TAGGED {tag: row.tag, timestamp: toInteger(row.timestamp)}]->(m)
        """
        session.run(query)
        print("TAGGED relationships created.")

# Fonction pour charger les scores de pertinence (HAS_TAG relations)
def create_has_tag_relationships():
    with driver.session() as session:
        query = """
        LOAD CSV WITH HEADERS FROM 'file:///genome-scores.csv' AS row
        MATCH (m:Movie {movieId: toInteger(row.movieId)})
        MATCH (t:Tag {tagId: toInteger(row.tagId)})
        CREATE (m)-[:HAS_TAG {relevance: toFloat(row.relevance)}]->(t)
        """
        session.run(query)
        print("HAS_TAG relationships created.")


# Charger les fichiers CSV dans Neo4j
def load_data():
    # Étape 1 : Créer les nœuds
    create_movies()  # Créer les nœuds de films
    create_links()  # Charger les liens IMDB et TMDB
    create_users()   # Créer les nœuds d'utilisateurs
    # create_tags()    # Créer les nœuds de tags

    # Étape 2 : Créer les relations
    create_rated_relationships()  # Créer les relations RATED
    create_tagged_relationships()  # Créer les relations TAGGED
    # create_has_tag_relationships()  # Créer les relations HAS_TAG

# Exécuter l'import des données
load_data()

# Fermer la connexion Neo4j
driver.close()
print("Connexion à Neo4j fermée.")

