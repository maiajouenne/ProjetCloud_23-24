import streamlit as st
import requests
import numpy as np
from anomaly_detection import detect_anomalies

# URL de base de votre API Flask
BASE_URL = "http://127.0.0.1:8080"

def fetch_sensor_data():
    """Récupère les 50 dernières données des capteurs depuis l'API."""
    response = requests.get(f"{BASE_URL}/data")
    if response.status_code == 200:
        data = response.json()[-50:]
        # Extrait les valeurs numériques de température et d'humidité
        temperatures = [float(entry['temperature']) for entry in data if entry['temperature'] != "information manquante"]
        humidities = [float(entry['humidity']) for entry in data if entry['humidity'] != "information manquante"]
        return data, np.array(temperatures), np.array(humidities)
    else:
        return [], [], []

def fetch_anomalies():
    """Récupère les anomalies détectées depuis l'API."""
    response = requests.get(f"{BASE_URL}/anomalies")
    if response.status_code == 200:
        anomalies = response.json()
        # Limite les résultats aux 20 dernières anomalies
        if len(anomalies) > 20:
            anomalies = anomalies[-20:]
        return anomalies
    else:
        return []

def display_sensor_data(data, outliers):
    """Affiche les données des capteurs avec les valeurs aberrantes en rouge."""
    for i, entry in enumerate(data):
        if outliers[i]:
            # Affiche en rouge si aberrant
            st.markdown(
                f"<span style='color: red;'>Plant ID: {entry['plant_id']}, "
                f"Sensor ID: {entry['sensor_id']}, Temp: {entry['temperature']}, "
                f"Humidity: {entry['humidity']}</span>", unsafe_allow_html=True)
        else:
            # Affichage normal
            st.text(f"Plant ID: {entry['plant_id']}, Sensor ID: {entry['sensor_id']}, "
                    f"Temp: {entry['temperature']}, Humidity: {entry['humidity']}")

def display_anomalies(data, outliers, anomalies):
    """Affiche les anomalies détectées et les valeurs aberrantes."""
    for i, entry in enumerate(data):
        if outliers[i]:
            st.text(f"Valeur aberrante détectée dans les données du capteur {entry['sensor_id']}: "
                    f"Temp: {entry['temperature']}, Humidity: {entry['humidity']}")

    for anomaly in anomalies:
        st.text(f"Anomalie dans les données du capteur {anomaly['sensor_data_id']}: {anomaly['description']}")

def main():
    st.title("Dashboard de la Ferme Urbaine")

    st.header("Données des Capteurs")
    data, temperatures, humidities = fetch_sensor_data()
    outliers = detect_anomalies(temperatures, humidities)

    display_sensor_data(data, outliers)

    st.header("Anomalies Détectées")
    anomalies = fetch_anomalies()
    display_anomalies(data, outliers, anomalies)

if __name__ == "__main__":
    main()
