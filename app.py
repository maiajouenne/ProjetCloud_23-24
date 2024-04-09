from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import base64
import msgpack

app = Flask(__name__)

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
    temperature = db.Column(db.Float, nullable=False, default=20.0)  # Valeur par défaut pour temperature
    humidity = db.Column(db.Float, nullable=False, default=50.0)      # Valeur par défaut pour humidity

class Anomaly(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_data_id = db.Column(db.Integer, db.ForeignKey('sensor_data.id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)

@app.route('/')
def index():
    return "L'API de la ferme urbaine est en cours d'exécution."

@app.route('/receive', methods=['POST'])
def receive_data():
    # Décoder la chaîne Base64 et désérialiser avec msgpack
    raw_data = request.get_data()
    base64_decoded = base64.b64decode(raw_data)
    data = msgpack.unpackb(base64_decoded, use_list=False, raw=False)
    
    # Utilisez les données désérialisées pour créer une nouvelle entrée SensorData
    new_data = SensorData(
        plant_id=data.get('plant_id'),
        sensor_id=data.get('sensor_id'),
        sensor_version=data.get('sensor_version'),
        temperature=data.get('temperature', 20.0),  # Utilisation de get() avec une valeur par défaut
        humidity=data.get('humidity', 50.0)         # Utilisation de get() avec une valeur par défaut
    )
    db.session.add(new_data)
    try:
        db.session.commit()
        return jsonify({"message": "Données reçues avec succès"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/data', methods=['GET'])
def get_data():
    data = SensorData.query.all()
    return jsonify([{'plant_id': d.plant_id, 'sensor_id': d.sensor_id, 'sensor_version': d.sensor_version,
                     'temperature': d.temperature, 'humidity': d.humidity} for d in data])

@app.route('/anomalies', methods=['GET'])
def get_anomalies():
    anomalies = Anomaly.query.all()
    return jsonify([{'sensor_data_id': a.sensor_data_id, 'description': a.description} for a in anomalies])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=8080)