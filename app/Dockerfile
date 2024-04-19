# Utiliser l'image officielle Python 3.11 avec Poetry pré-installé
FROM python:3.11-slim

# Installer Poetry
RUN pip install --no-cache-dir poetry

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier seulement les fichiers nécessaires à l'installation des dépendances
COPY pyproject.toml poetry.lock /app/

# Installer les dépendances sans créer de virtual envs, utilisation du système directement
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copier le reste des fichiers de l'application
COPY app/app.py /app/

# Commande par défaut pour démarrer l'application
CMD ["poetry", "run", "python", "app.py"]
