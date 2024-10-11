# project_movie

Pour lancer le projet sur docker Desktop


cd backend 

Créer un .env avec

NEO4J_USER=neo4j
NEO4J_PASS=123456789
NEO4J_URI=bolt://localhost:7687

docker-compose up --build

localhost:3000   pour le Frontend
localhost:5000   pour le Backend
