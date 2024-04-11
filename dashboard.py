import streamlit as st
import requests

# URL de base de votre API Flask
BASE_URL = "http://127.0.0.1:5000"

def fetch_sensor_data():
    """Récupère les 50 dernières données des capteurs depuis l'API."""
    response = requests.get(f"{BASE_URL}/data")
    if response.status_code == 200:
        # Obtient uniquement les 50 dernières données
        return response.json()[-50:]
    else:
        return []

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



def display_sensor_data(data):
    """Affiche les données des capteurs avec les valeurs aberrantes en rouge."""
    for entry in data:
        try:
            # Essayer de convertir la température en float pour la comparaison
            temp = float(entry['temperature'])
            temp_aberrant = temp < -10 or temp > 50
        except ValueError:
            # Si la conversion échoue, définir temp_aberrant à False
            temp_aberrant = False

        try:
            # Même processus pour l'humidité
            humid = float(entry['humidity'])
            humid_aberrant = humid < 0 or humid > 100
        except ValueError:
            humid_aberrant = False

        # Affiche les données en rouge si temp_aberrant ou humid_aberrant est vrai
        if temp_aberrant or humid_aberrant:
            st.markdown(
                f"<span style='color: red;'>Plant ID: {entry['plant_id']}, "
                f"Sensor ID: {entry['sensor_id']}, Temp: {entry['temperature']}, "
                f"Humidity: {entry['humidity']}</span>", unsafe_allow_html=True)
        else:
            st.text(f"Plant ID: {entry['plant_id']}, Sensor ID: {entry['sensor_id']}, "
                    f"Temp: {entry['temperature']}, Humidity: {entry['humidity']}")



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
