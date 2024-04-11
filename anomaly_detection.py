from sklearn.neighbors import LocalOutlierFactor
import numpy as np

def detect_anomalies(temperature, humidity, n_neighbors=35, contamination='auto'):
    """Détecte les anomalies dans les données de température et d'humidité à l'aide de l'algorithme Local Outlier Factor (LOF)."""
    data = np.column_stack((temperature, humidity))

    clf = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=contamination)
    y_pred = clf.fit_predict(data)
    anomalies = y_pred == -1

    return anomalies
