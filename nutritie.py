import streamlit as st
import pandas as pd
import plotly.express as px

# Configurare Pagina
st.set_page_config(page_title="NutriFit Pro", layout="wide")

# Sistem de Parolă Simplu
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def check_password():
    if st.sidebar.text_input("Parolă", type="password") == "nutrifit2026":
        st.session_state["authenticated"] = True
    else:
        if st.session_state["authenticated"] == False:
            st.error("🔒 Acces restricționat. Introdu parola în lateral.")

check_password()

if st.session_state["authenticated"]:
    st.title("🍎 NutriFit Pro - Calculator Nutrițional")
    
    col1, col2 = st.columns(2)
    
    with col1:
        nume = st.text_input("Nume Client")
        greutate = st.number_input("Greutate (kg)", min_value=40.0, max_value=200.0, value=70.0)
        obiectiv = st.selectbox("Obiectiv", ["Slăbire", "Menținere", "Masă Musculară"])
    
    with col2:
        protein_pct = st.slider("Proteine (%)", 10, 40, 30)
        carbs_pct = st.slider("Carbohidrați (%)", 10, 60, 40)
        fats_pct = 100 - (protein_pct + carbs_pct)
        st.info(f"Grăsimi calculate automat: {fats_pct}%")

    # Calcul Caloric Simplist (Exemplu)
    kcal = greutate * 30 if obiectiv == "Menținere" else (greutate * 25 if obiectiv == "Slăbire" else greutate * 35)
    
    st.success(f"### Total Calorii Recomandate: {int(kcal)} kcal")
    
    # Grafic
    df_macros = pd.DataFrame({
        "Macro": ["Proteine", "Carbohidrați", "Grăsimi"],
        "Valoare": [protein_pct, carbs_pct, fats_pct]
    })
    fig = px.pie(df_macros, values='Valoare', names='Macro', title="Distribuție Macronutrienți")
    st.plotly_chart(fig)