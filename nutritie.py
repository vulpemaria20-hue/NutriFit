import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURARE PAGINĂ (Trebuie să fie prima instrucțiune Streamlit)
st.set_page_config(page_title="NutriFit Pro: Aplicația Mariei", layout="wide", page_icon="🍎")

# 2. SECURITATE (Varianta corectă)
if "autentificat" not in st.session_state:
    st.session_state.autentificat = False

if not st.session_state.autentificat:
    st.title("🔒 Acces Protejat NutriFit")
    parola = st.text_input("Introdu parola pentru deblocare:", type="password")
    if st.button("Autentificare"):
        if parola == "nutrifit2026":
            st.session_state.autentificat = True
            st.rerun()
        else:
            st.error("Parolă incorectă! Contactează administratorul.")
    st.stop() # Oprește execuția restului codului dacă nu e logat

# 3. INTERFAȚĂ APLICAȚIE (Apare doar după logare)
st.title("🍎 NutriFit Pro: Aplicația Mariei")

if 'calculat' not in st.session_state:
    st.session_state.calculat = False

tab1, tab2, tab3 = st.tabs(["📊 Calculator & Macros", "🍱 Meniu pe 7 Zile", "🛒 Lista de Cumpărături"])

# --- TAB 1: CALCULATOR ---
with tab1:
    col_in, col_out = st.columns([1, 2], gap="large")
    
    with col_in:
        st.subheader("📝 Date Profil")
        greutate = st.number_input("Greutate (kg)", 40.0, 200.0, 75.0)
        sex = st.radio("Sex", ["Masculin", "Feminin"], horizontal=True)
        
        activitate_optiuni = {
            "Sedentar (Birou)": 1.2,
            "Activitate Ușoară": 1.375, 
            "Moderat Activ": 1.55, 
            "Foarte Activ": 1.725
        }
        nivel = st.selectbox("Nivel de Activitate:", list(activitate_optiuni.keys()))
        factor = activitate_optiuni[nivel]
        
        tip = st.selectbox("Tip Somatic:", ["Ectomorf", "Mezomorf", "Endomorf"])
        
        if st.button("CALCULEAZĂ PLANUL"):
            # Calcul Rata Metabolică Bazală (RMB) - formulă simplificată
            rmb = (10 * greutate) + (6.25 * 165) - (5 * 30) + (5 if sex == "Masculin" else -161)
            necesar = int(rmb * factor)
            deficit = necesar - 500 # Deficit standard pentru slăbire
            
            st.session_state.calculat = True
            st.session_state.necesar = necesar
            st.session_state.deficit = deficit

    with col_out:
        if st.session_state.get('calculat'):
            st.subheader("🎯 Rezultate Plan")
            st.metric("Necesar Menținere", f"{st.session_state.necesar} kcal")
            st.metric("Țintă Slăbire (Deficit)", f"{st.session_state.deficit} kcal", delta="-500 kcal")
            
            # Exemplu Grafic Macros
            df_macros = pd.DataFrame({
                "Macro": ["Proteine", "Carbohidrați", "Grăsimi"],
                "Valoare": [30, 40, 30]
            })
            fig = px.pie(df_macros, values='Valoare', names='Macro', title="Distribuție Macronutrienți (%)")
            st.plotly_chart(fig)
        else:
            st.info("Introdu datele și apasă butonul de calcul.")

# --- TAB 2 & 3 (Schițe) ---
with tab2:
    st.subheader("🍱 Meniu personalizat")
    st.write("Aici va apărea meniul tău după ce finalizăm algoritmul.")

with tab3:
    st.subheader("🛒 Ce trebuie să cumperi")
    st.write("Lista de cumpărături generată automat.")
