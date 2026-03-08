import os
os.system("pip install plotly")
import plotly.express as px
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configurare Pagina
st.set_page_config(page_title="Aplicatia Mariei ", layout="wide")

# 2. Sistem de Parolă în Sidebar
st.sidebar.title("🔐 Autentificare")
parola = st.sidebar.text_input("Introdu parola proiectului:", type="password")

if parola == "nutrifit2026":
    st.title("🍎Aplicatia Mariei  - Dashboard Nutrițional")
    st.markdown("---")

    # 3. Introducere Date Client
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👤 Date Client")
        nume = st.text_input("Nume complet:")
        greutate = st.number_input("Greutate actuală (kg):", 40, 200, 70)
        obiectiv = st.selectbox("Obiectivul tău:", ["Slăbire", "Menținere", "Masă Musculară"])
    
    with col2:
        st.subheader("⚖️ Setare Macronutrienți (%)")
        proteine = st.slider("Proteine (%)", 10, 40, 25)
        carbohidrati = st.slider("Carbohidrați (%)", 10, 60, 45)
        grasimi = 100 - (proteine + carbohidrati)
        st.info(f"Grăsimi calculate automat: **{grasimi}%**")

    # 4. Calcule Matematice
    if obiectiv == "Slăbire":
        total_kcal = greutate * 24
    elif obiectiv == "Masă Musculară":
        total_kcal = greutate * 35
    else:
        total_kcal = greutate * 30

    st.markdown("---")
    st.success(f"### 🔥 Total Calorii Recomandate: {int(total_kcal)} kcal / zi")

    # 5. Generare Grafic (Aici era eroarea!)
    st.subheader("📊 Distribuția Caloriilor")
    date_grafic = pd.DataFrame({
        "Nutrient": ["Proteine", "Carbohidrați", "Grăsimi"],
        "Procent": [proteine, carbohidrati, grasimi]
    })
    
    fig = px.pie(date_grafic, values='Procent', names='Nutrient', 
                 color_discrete_sequence=px.colors.sequential.RdBu,
                 hole=0.4)
    
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Te rugăm să introduci parola corectă în meniul din stânga pentru a debloca instrumentele.")
    st.info("Sfat: Parola este 'nutrifit2026'")




