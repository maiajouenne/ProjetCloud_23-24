# Utiliser une image de base Python officielle
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY pyproject.toml poetry.lock* /app/

# Installer Poetry et les dépendances du projet
RUN pip install poetry && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copier les autres fichiers nécessaires
COPY . /app

# Exposer le port sur lequel l'application s'exécute
EXPOSE 5000

# Définir la commande pour exécuter l'application
CMD ["python", "app.py"]