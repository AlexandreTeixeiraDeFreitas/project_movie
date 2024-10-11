from neo4j import GraphDatabase

class Neo4jClient:
    def __init__(self, driver):
        self.driver = driver

    def close(self):
        self.driver.close()

    def get_movie_info(self, movie_id, page=1, page_size=25):
        skip_count = (page - 1) * page_size
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (m:Movie {movieId: $movie_id})
                OPTIONAL MATCH (m)<-[r:RATED]-(u:User)
                OPTIONAL MATCH (m)<-[t:TAGGED]-(u2:User)
                WITH m, u.userId AS UserId, r.rating AS Rating, collect(t.tag) AS Tags
                WITH m, collect({
                    userId: UserId,
                    rating: Rating,
                    tags: Tags
                }) AS UsersInfo
                RETURN m.movieId AS MovieID,
                    m.title AS Title,
                    split(m.genres, '|') AS Genres,
                    m.imdbId AS IMDB_ID,
                    m.tmdbId AS TMDB_ID,
                    UsersInfo[$skip_count..$limit_count] AS PaginatedUsersInfo
                """,
                movie_id=movie_id,
                skip_count=skip_count,
                limit_count=skip_count + page_size
            )
            record = result.single()
            if record:
                return {
                    "movieId": record["MovieID"],
                    "title": record["Title"],
                    "genres": record["Genres"],
                    "imdbId": record["IMDB_ID"],
                    "tmdbId": record["TMDB_ID"],
                    "usersInfo": record["PaginatedUsersInfo"]
                }
            else:
                return None


    # Fonction pour récupérer les films avec tags, genres et moyenne des évaluations avec pagination
    def get_movies_with_tags_and_avg_rating(self, page=1, page_size=25):
        skip_count = (page - 1) * page_size
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (m:Movie)
                OPTIONAL MATCH (m)<-[:TAGGED]-(u:User)  // Récupère les tags associés aux films via les utilisateurs
                OPTIONAL MATCH (m)<-[r:RATED]-(u2:User)  // Récupère les évaluations pour chaque film
                WITH m, collect(DISTINCT u.tag) AS tags, avg(r.rating) AS AverageRating  // Calcule la moyenne des évaluations et collecte les tags
                RETURN m.movieId AS movieId,
                    m.title AS title, 
                    tags, 
                    split(m.genres, '|') AS GenresArray,  // Divise la chaîne de genres en tableau
                    coalesce(AverageRating, 0) AS AverageRating  // Utilise '0' s'il n'y a pas d'évaluations
                SKIP $skip_count LIMIT $page_size
                """,
                skip_count=skip_count,
                page_size=page_size
            )
            data = result.data()
            print(data)  # Affiche la réponse pour vérifier les données
            return data
        
    # Fonction pour récupérer tous les tags distincts et les trier par ordre alphabétique
    def get_distinct_tags(self):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (m:Movie)<-[t:TAGGED]-(u:User)
                RETURN DISTINCT t.tag AS Tag
                ORDER BY Tag
                """
            )
            return [record["Tag"] for record in result]
        
    # Nouvelle fonction pour récupérer les genres distincts
    def get_distinct_genres(self):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (m:Movie)
                WITH m, split(m.genres, '|') AS genreList  // Décompose les genres
                UNWIND genreList AS genre  // Sépare chaque genre en une ligne distincte
                RETURN DISTINCT genre  // Récupère uniquement les genres distincts
                ORDER BY genre
                """
            )
            return [record["genre"] for record in result]
    
     

    # Fonction pour récupérer les films par tag spécifique avec pagination
    def get_movies_by_tag(self, tag, page=1, page_size=25):
        skip_count = (page - 1) * page_size
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (m:Movie)<-[t:TAGGED]-(u:User)
                WHERE t.tag = $tag  // Filtrer par tag spécifique
                OPTIONAL MATCH (m)<-[r:RATED]-(u2:User)
                WITH m, collect(DISTINCT t.tag) AS tags, avg(r.rating) AS AverageRating
                RETURN m.movieId AS movieId,  // Utilisez 'movieId' pour correspondre aux autres méthodes
                    m.title AS title,     // Utilisez 'title' pour correspondre aux autres méthodes
                    tags, 
                    split(m.genres, '|') AS GenresArray,  // Divise la chaîne de genres en tableau
                    coalesce(AverageRating, 0) AS AverageRating  // Utilise '0' s'il n'y a pas d'évaluations
                SKIP $skip_count LIMIT $page_size
                """,
                tag=tag,
                skip_count=skip_count,
                page_size=page_size
            )
            data = result.data()
            print(data)  # Affiche la réponse pour vérifier les données
            return data

        

    # Fonction pour récupérer les films qui contiennent tous les genres spécifiés, avec pagination
    def get_movies_by_genres(self, genres_list, page=1, page_size=25):
        skip_count = (page - 1) * page_size
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (m:Movie)
                WHERE ALL(genre IN $genres_list 
                        WHERE genre IN split(m.genres, '|'))  // Vérifie si tous les genres spécifiés sont présents
                OPTIONAL MATCH (m)<-[:TAGGED]-(u:User)  // Récupère les tags associés aux films via les utilisateurs
                OPTIONAL MATCH (m)<-[r:RATED]-(u2:User)  // Récupère les évaluations pour chaque film
                WITH m, collect(DISTINCT u.tag) AS tags, avg(r.rating) AS AverageRating  // Calcule la moyenne des évaluations et collecte les tags
                RETURN m.movieId AS movieId,
                    m.title AS title, 
                    tags, 
                    split(m.genres, '|') AS GenresArray,  // Divise la chaîne de genres en tableau
                    coalesce(AverageRating, 0) AS AverageRating  // Utilise '0' s'il n'y a pas d'évaluations
                SKIP $skip_count LIMIT $page_size
                """,
                genres_list=genres_list,
                skip_count=skip_count,
                page_size=page_size
            )
            data = result.data()
            print(data)  # Affiche la réponse pour vérifier les données
            return data

        
    # Fonction pour récupérer les films dont le titre contient une chaîne, avec pagination
    def search_movies_by_title(self, search_term, page=1, page_size=25):
        skip_count = (page - 1) * page_size
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (m:Movie)
                WHERE toLower(m.title) CONTAINS toLower($search_term)
                OPTIONAL MATCH (m)<-[:TAGGED]-(u:User)  // Récupère les tags associés aux films via les utilisateurs
                OPTIONAL MATCH (m)<-[r:RATED]-(u2:User)  // Récupère les évaluations pour chaque film
                WITH m, collect(DISTINCT u.tag) AS tags, avg(r.rating) AS AverageRating  // Calcule la moyenne des évaluations et collecte les tags
                RETURN m.movieId AS movieId,
                    m.title AS title, 
                    tags, 
                    split(m.genres, '|') AS GenresArray,  // Divise la chaîne de genres en tableau
                    coalesce(AverageRating, 0) AS AverageRating  // Utilise '0' s'il n'y a pas d'évaluations
                SKIP $skip_count LIMIT $page_size
                """,
                search_term=search_term,
                skip_count=skip_count,
                page_size=page_size
            )
            data = result.data()
            print(data)  # Affiche la réponse pour vérifier les données
            return data

