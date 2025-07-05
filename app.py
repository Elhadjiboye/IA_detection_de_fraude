from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Charger le modèle sauvegardé
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Route d'accueil (optionnelle)
@app.route('/')
def home():
    return "API de détection de fraude est en ligne"

# Route /predict qui reçoit les données en JSON et renvoie la prédiction
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    # Exemple : les données doivent être un dict avec les features en clé/valeur
    # Ex: {"Gender":0, "Age":45, "HouseTypeID":1, ..., "TransactionCurrencyCode":3}

    # Extraire les features dans le bon ordre
    features_order = ['Gender', 'Age', 'HouseTypeID', 'ContactAvaliabilityID', 'HomeCountry',
                      'AccountNo', 'CardExpiryDate', 'TransactionAmount', 'TransactionCountry',
                      'LargePurchase', 'ProductID', 'CIF', 'TransactionCurrencyCode']

    try:
        input_data = [data[feature] for feature in features_order]
    except KeyError as e:
        return jsonify({'error': f'Missing feature: {str(e)}'}), 400

    # Convertir en DataFrame (1 ligne)
    input_df = pd.DataFrame([input_data], columns=features_order)

    # Ici tu peux appliquer la même normalisation que pour l'entraînement, si besoin.
    # Par exemple, si tu as un scaler sauvegardé, tu peux le charger et appliquer transform
    # input_df = scaler.transform(input_df)

    # Prédiction
    prediction = model.predict(input_df)[0]

    # Retourner le résultat JSON
    return jsonify({'prediction': int(prediction)})

if __name__ == '__main__':
    app.run(host='0.0.0.0',
        port=3000 ,debug=True)
