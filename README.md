# Système de Collecte de Données pour Ferme Urbaine

Ce projet comprend un système de collecte de données pour une ferme urbaine, utilisant une API Flask, Prometheus et Grafana pour le monitoring, ainsi que Docker pour la conteneurisation. Le système collecte des données à partir de divers capteurs, les traite et les stocke, détecte les anomalies et fournit des outils de monitoring visuels.

## Structure du Projet

- `app.py` : Application Flask pour la réception et le traitement des données des capteurs.
- `dashboard.py` : Application Streamlit pour afficher les données et les anomalies détectées.
- `anomaly_detection.py` : Contient la logique de détection d'anomalies.
- `docker-compose.yml` : Fichier Docker Compose pour orchestrer la simulation des capteurs et l'API de collecte de données.
- `prometheus.yml` : Configuration pour le monitoring Prometheus.
- Fichiers de déploiement et de service pour le déploiement Kubernetes.
- `pyproject.toml` : Fichier de dépendances Poetry.

## Installation

Assurez-vous d'avoir Docker, Docker Compose et Poetry installés sur votre système.

### API Backend

1. Installez les dépendances du projet en utilisant Poetry :
   ```sh
   poetry install

Activez l'environnement virtuel : 
poetry shell

2. Démarrez l'API Flask :
python app.py

Simulation des Capteurs
Exécutez les capteurs avec Docker Compose :
docker-compose up -d


Déploiement Kubernetes (Optionnel)
Déployez les services sur Kubernetes (en supposant que Minikube est utilisé) :
minikube start
kubectl apply -f deployment/
kubectl apply -f service/

Accédez aux services :
minikube service grafana-service
minikube service prometheus-service

Utilisation
Une fois que tout est en cours d'exécution, vous pouvez accéder au tableau de bord Streamlit pour voir les données des capteurs et les anomalies :
streamlit run dashboard.py

Le tableau de bord doit être accessible à http://localhost:8501.

Prometheus et Grafana sont disponibles à http://localhost:9090 et http://localhost:3000, respectivement.

Services/déploiement Kubernetes:
kubectl apply -f service/
kubectl apply -f deployment/

