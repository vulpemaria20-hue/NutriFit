import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURARE PAGINĂ
st.set_page_config(page_title="Aplicația Mariei", layout="wide", page_icon="🍎")

# 2. SECURITATE
if "autentificat" not in st.session_state:
    st.session_state.autentificat = False

if not st.session_state.autentificat:
    st.title("🔒 Acces Protejat")
    parola = st.text_input("Introdu parola:", type="password")
    if st.button("Autentificare"):
        if parola == "nutrifit2026":
            st.session_state.autentificat = True
            st.rerun()
        else:
            st.error("Parolă incorectă!")
    st.stop()

# 3. INTERFAȚĂ (Am scos titlurile cu Nutrifit)
st.title("🍎 Aplicația Mariei")

if 'calculat' not in st.session_state:
    st.session_state.calculat = False

tab1, tab2, tab3 = st.tabs(["📊 Calculator & Macros", "🍱 Meniu pe 7 Zile", "🛒 Lista de Cumpărături"])

with tab1:
    col_in, col_out = st.columns([1, 2], gap="large")
    with col_in:
        st.subheader("📝 Date Profil")
        greutate = st.number_input("Greutate (kg)", 40.0, 200.0, 75.0)
        sex = st.radio("Sex", ["Masculin", "Feminin"], horizontal=True)
        
        activitate_optiuni = {"Sedentar": 1.2, "Activitate Ușoară": 1.375, "Moderat": 1.55, "Activ": 1.725}
        nivel = st.selectbox("Nivel de Activitate:", list(activitate_optiuni.keys()))
        
        if st.button("CALCULEAZĂ PLANUL"):
            rmb = (10 * greutate) + (6.25 * 165) - (5 * 30) + (5 if sex == "Masculin" else -161)
            necesar = int(rmb * activitate_optiuni[nivel])
            st.session_state.necesar = necesar
            st.session_state.deficit = necesar - 500
            st.session_state.calculat = True

    with col_out:
        if st.session_state.calculat:
            st.subheader("🎯 Rezultate")
            st.metric("Necesar Menținere", f"{st.session_state.necesar} kcal")
            st.metric("Țintă Slăbire", f"{st.session_state.deficit} kcal")

# --- TAB 2: AICI PUNEM MENIUL TĂU ---
with tab2:
    st.subheader("🍱 Meniu Personalizat")
    
    # Exemplu de tabel pentru meniu (îl poți edita)
    date_meniu = {
        "Ziua": ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"],
        "Mic Dejun": ["Omletă", "Iaurt cu ovăz", "Pancakes proteice", "Omletă", "Smoothie", "Ouă ochiuri", "Iaurt"],
        "Prânz": ["Pui cu orez", "Pește cu legume", "Vită", "Pui cu orez", "Salată cu ton", "Curcan", "Gratar"],
        "Cină": ["Salată", "Supă cremă", "Brânză cu roșii", "Salată verde", "Iaurt", "Pește", "Salată"]
    }
    df_meniu = pd.DataFrame(date_meniu)
    st.table(df_meniu) # Afișează meniul sub formă de tabel curat

with tab3:
    st.subheader("🛒 Lista de Cumpărături")
    st.write("- Piept de pui\n- Ouă\n- Legume verzi\n- Iaurt grecesc")
