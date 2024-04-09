import streamlit as st
import requests

# URL de base de votre API Flask
BASE_URL = "http://127.0.0.1:5000/"

def fetch_sensor_data():
    """Récupère les données des capteurs depuis l'API."""
    response = requests.get(f"{BASE_URL}/data")
    if response.status_code == 200:
        return response.json()
    else:
        return []

def fetch_anomalies():
    """Récupère les anomalies détectées depuis l'API."""
    response = requests.get(f"{BASE_URL}/anomalies")
    if response.status_code == 200:
        return response.json()
    else:
        return []

def display_sensor_data(data):
    """Affiche les données des capteurs."""
    for entry in data:
        st.text(f"Plant ID: {entry['plant_id']}, Sensor ID: {entry['sensor_id']}, Temp: {entry['temperature']}, Humidity: {entry['humidity']}")

def display_anomalies(anomalies):
    """Affiche les anomalies détectées."""
    for anomaly in anomalies:
        st.text(f"Anomalie détectée dans les données du capteur {anomaly['sensor_data_id']}: {anomaly['description']}")

def main():
    st.title("Dashboard de la Ferme Urbaine")

    st.header("Données des Capteurs")
    sensor_data = fetch_sensor_data()
    display_sensor_data(sensor_data)

    st.header("Anomalies Détectées")
    anomalies = fetch_anomalies()
    display_anomalies(anomalies)

if __name__ == "__main__":
    main()
