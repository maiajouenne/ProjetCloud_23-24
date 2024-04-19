# Utiliser l'image officielle de Python
FROM python:3.11-slim

# Mettre à jour pip
RUN pip install --upgrade pip
RUN pip freeze
RUN pip install --no-cache-dir streamlit numpy pandas scikit-learn

# Copier les fichiers du dashboard
WORKDIR /dashboard
COPY dashboard/dashboard.py /dashboard/
COPY dashboard/anomaly_detection.py /dashboard/

# Exposer le port 8501 
EXPOSE 8501

# Commande pour démarrer Streamlit
CMD ["streamlit", "run", "dashboard.py", "--server.address", "0.0.0.0"]
