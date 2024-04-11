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
        # Définition des seuils d'aberration
        temp_aberrant = entry['temperature'] < -10 or entry['temperature'] > 50
        humid_aberrant = entry['humidity'] < 0 or entry['humidity'] > 100

        if temp_aberrant or humid_aberrant:
            # Affiche en rouge si aberrant
            st.markdown(
                f"<span style='color: red;'>Plant ID: {entry['plant_id']}, "
                f"Sensor ID: {entry['sensor_id']}, Temp: {entry['temperature']}, "
                f"Humidity: {entry['humidity']}</span>", unsafe_allow_html=True)
        else:
            # Affichage normal
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
