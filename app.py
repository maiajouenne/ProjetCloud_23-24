from flask import Flask, request, jsonify, response
from flask_sqlalchemy import SQLAlchemy
import os
import base64
import msgpack
import re
from msgpack.exceptions import ExtraData, UnpackValueError
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import start_http_server, Summary, Counter, Gauge, generate_latest

app = Flask(__name__)
metrics = PrometheusMetrics(app)  # Initialise Prometheus metrics collection

# static information as metric
metrics.info('app_info', 'Application info', version='1.0.3')

# Configuration du chemin vers le dossier 'instance' pour la base de données
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'sensor_data.db')

# Configuration de la base de données avec un chemin absolu
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, nullable=False)
    sensor_id = db.Column(db.String(80), nullable=False)
    sensor_version = db.Column(db.String(80), nullable=False)
    temperature = db.Column(db.String, nullable=True)
    humidity = db.Column(db.String, nullable=True)

class Anomaly(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_data_id = db.Column(db.Integer, db.ForeignKey('sensor_data.id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)

@app.route('/')
def index():
    return "L'API de la ferme urbaine est en cours d'exécution."

@app.route('/receive', methods=['POST'])
def receive_data():
    raw_data = request.get_data().strip()

    # Nettoyage des données brutes à l'aide d'expressions régulières
    cleaned_data = re.sub(r'^/', '', raw_data.decode('utf-8').strip())  # Supprime le slash initial si présent
    cleaned_data = re.sub(r'ICA=a', '', cleaned_data)  # Supprime 'ICA=a' s'il est présent
    cleaned_data = re.sub(r'ICA=', '', cleaned_data)  # Supprime 'ICA=' s'il est présent

    try:
        base64_decoded = base64.b64decode(cleaned_data)
        data = msgpack.unpackb(base64_decoded, raw=False)
        if not isinstance(data, dict):
            raise ValueError("Les données doivent être un dictionnaire.")
    except (ExtraData, ValueError) as e:
        record_anomaly("inconnu", f"Erreur lors de la désérialisation des données : {str(e)}")
        return jsonify({"error": "Format de données invalide"}), 400
    except UnpackValueError as e:
        record_anomaly("inconnu", f"Erreur de décodage MsgPack : {str(e)}")
        return jsonify({"error": "Erreur de décodage MsgPack"}), 400
    
    # Traitement des données valides
    measures = data.get('measures', {})

    temperature_celsius = None
    temp_keys = ['temperature', 'température']
    for key in temp_keys:
        if key in measures:
            temp_value = measures[key]
            if '°C' in temp_value:
                temperature_celsius = float(temp_value.replace('°C', ''))
            elif '°F' in temp_value:
                temperature_celsius = (float(temp_value.replace('°F', '')) - 32) * 5.0 / 9.0
            elif '°K' in temp_value:
                temperature_celsius = float(temp_value.replace('°K', '')) - 273.15
            break

    humidity_percent = None
    humid_keys = ['humidity', 'humidite']
    for key in humid_keys:
        if key in measures:
            humidity_value = measures[key]
            humidity_percent = float(humidity_value.replace('%', ''))
            break

    # Enregistrement des anomalies pour les valeurs aberrantes
    if temperature_celsius and (temperature_celsius < -10 or temperature_celsius > 50):
        record_anomaly(data.get('sensor_id'), f"Température aberrante détectée: {temperature_celsius}°C")

    if humidity_percent and (humidity_percent < 0 or humidity_percent > 100):
        record_anomaly(data.get('sensor_id'), f"Humidité aberrante détectée: {humidity_percent}%")

    # Création et enregistrement des données valides avec gestion des valeurs manquantes
    new_data = SensorData(
        plant_id=data.get('plant_id'),
        sensor_id=data.get('sensor_id'),
        sensor_version=data.get('sensor_version'),
        temperature=str(temperature_celsius) if temperature_celsius is not None else "information manquante",
        humidity=str(humidity_percent) if humidity_percent is not None else "information manquante"
    )
    db.session.add(new_data)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        record_anomaly(data.get('sensor_id'), f"Erreur lors de l'enregistrement des données : {str(e)}")

    return jsonify({"message": "Données reçues avec succès"}), 201

@app.route('/data', methods=['GET'])
def get_data():
    data = SensorData.query.all()
    result = [{
        'plant_id': d.plant_id,
        'sensor_id': d.sensor_id,
        'sensor_version': d.sensor_version,
        'temperature': d.temperature,
        'humidity': d.humidity
    } for d in data]
    return jsonify(result)

@app.route('/anomalies', methods=['GET'])
def get_anomalies():
    anomalies = Anomaly.query.all()
    result = [{'sensor_data_id': a.sensor_data_id, 'description': a.description} for a in anomalies]
    return jsonify(result)

def record_anomaly(sensor_id, description):
    anomaly = Anomaly(sensor_data_id=sensor_id, description=description)
    db.session.add(anomaly)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Erreur lors de l'enregistrement de l'anomalie: {e}")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
