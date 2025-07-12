import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Détection de Fraude", layout="wide", page_icon="🔍")

st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🔍 Détection de Fraude Bancaire</h1>", unsafe_allow_html=True)
st.markdown("**Remplissez les informations ci-dessous pour détecter une fraude potentielle.**")

# Initialiser l'historique de session
if "history" not in st.session_state:
    st.session_state.history = []

# Layout des champs de saisie
with st.form("fraude_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        gender = st.selectbox("🎭 Genre", [0, 1])
        age = st.number_input("🎂 Âge", min_value=18, max_value=100, value=30)
        house_type_id = st.number_input("🏠 Type de logement (ID)", min_value=0, value=1)
        contact_availability_id = st.selectbox("📞 Contact disponible", [0, 1])

    with col2:
        home_country = st.selectbox("🌍 Pays d’origine", [0, 1])
        account_no = st.number_input("🏦 Numéro de compte", value=123456)
        card_expiry = st.number_input("💳 Expiration de carte (YYYYMM)", value=202512)
        transaction_amount = st.number_input("💰 Montant de la transaction", value=150.00)

    with col3:
        transaction_country = st.selectbox("🌐 Pays de transaction", [0, 1])
        large_purchase = st.selectbox("🛍️ Achat important", [0, 1])
        product_id = st.number_input("📦 Product ID", value=10001)
        cif = st.number_input("🧾 CIF", value=2002)
        transaction_currency = st.selectbox("💱 Devise", [0, 1])

    submit_btn = st.form_submit_button("🔎 Lancer la prédiction")

# === Prédiction
if submit_btn:
    data = {
        "Gender": gender,
        "Age": age,
        "HouseTypeID": house_type_id,
        "ContactAvaliabilityID": contact_availability_id,
        "HomeCountry": home_country,
        "AccountNo": account_no,
        "CardExpiryDate": card_expiry,
        "TransactionAmount": transaction_amount,
        "TransactionCountry": transaction_country,
        "LargePurchase": large_purchase,
        "ProductID": product_id,
        "CIF": cif,
        "TransactionCurrencyCode": transaction_currency
    }

    try:
        url = "https://ia-detection-de-fraude.onrender.com/predict"
        response = requests.post(url, json=data)
        prediction = response.json().get("prediction")

        st.session_state.history.append(prediction)

        if prediction == 1:
            st.markdown("<div style='background-color:#ffe6e6;padding:20px;border-radius:10px'><h3 style='color:#D8000C;'>⚠️ Risque de fraude détecté</h3></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='background-color:#e6ffea;padding:20px;border-radius:10px'><h3 style='color:#2e7d32;'>✅ Aucune fraude détectée</h3></div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Erreur lors de l'appel à l'API : {e}")

# === Statistiques
if st.session_state.history:
    st.markdown("### 📊 Statistiques de cette session")
    df_hist = pd.DataFrame(st.session_state.history, columns=["Prediction"])
    counts = df_hist["Prediction"].value_counts().sort_index()

    # Affichage sous forme de dashboard
    col1, col2 = st.columns(2)
    col1.metric("Nombre sans fraude (0)", counts.get(0, 0), help="Transactions normales")
    col2.metric("Nombre avec fraude (1)", counts.get(1, 0), help="Transactions suspectes")

    # Diagramme circulaire
    pie_df = df_hist["Prediction"].map({0: "Sans Fraude", 1: "Fraude"}).value_counts().reset_index()
    pie_df.columns = ["Classe", "Nombre"]

    fig = px.pie(pie_df, names="Classe", values="Nombre", title="Répartition des prédictions", color_discrete_sequence=["#4CAF50", "#F44336"])
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)
