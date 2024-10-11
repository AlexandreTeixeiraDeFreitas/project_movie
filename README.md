Voici le README mis à jour avec l'ajout de l'étape concernant le script `project_import.py` :

---

# Project Movie

## Lancer le projet avec Docker Desktop

### Étape 1 : Configuration du back-end

1. Accédez au répertoire du backend :
   ```bash
   cd backend
   ```

2. Créez un fichier nommé `.env` et ajoutez-y les variables d'environnement suivantes :
   ```
   NEO4J_USER=neo4j
   NEO4J_PASS=123456789
   NEO4J_URI=bolt://localhost:7687
   ```

### Étape 2 : Modification du fichier docker-compose.yaml

Avant de lancer le projet avec Docker, vous devez modifier une ligne dans le fichier `docker-compose.yaml`. 

- Remplacez cette ligne :
   ```
   - C:/xampp/htdocs/project_movie/datacsv:/var/lib/neo4j/import
   ```

- Par votre propre chemin absolu vers le répertoire `datacsv` :
   ```
   - VOTRE_CHEMIN_ABSOLU_VERS_DATACSV:/var/lib/neo4j/import
   ```

⚠️ **Important :** Assurez-vous de conserver les deux-points `:` dans la syntaxe.

### Étape 3 : Importation des données dans Neo4j

Exécutez le script `project_import.py` pour remplir la base de données Neo4j avec les données issues des fichiers CSV. Ce processus prend entre 3 et 6 minutes.

```bash
python project_import.py
```

### Étape 4 : Lancer le projet

Lancez le projet avec Docker en utilisant la commande suivante :
```bash
docker-compose up --build
```

### Accéder à l'application

- Frontend : [localhost:3000](http://localhost:3000)
- Backend : [localhost:5000](http://localhost:5000)

---

Cette version inclut l'étape pour exécuter le script d'importation des données, ce qui rend le guide plus complet et précis.
