import streamlit as st

def verifica_parola():
    if "autentificat" not in st.session_state:
        st.session_state["autentificat"] = False

    if not st.session_state["autentificat"]:
        parola_introdusa = st.text_input("Introdu parola pentru acces:", type="password")
        if st.button("Logare"):
            if parola_introdusa == "ParolaTaSecreta123":
                st.session_state["autentificat"] = True
                st.rerun()
            else:
                st.error("Parolă incorectă!")
        return False
    return True

if verifica_parola():
    # AICI pui tot codul aplicației tale NutriFit
    st.title("Bine ai venit la NutriFit!")
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURARE PAGINĂ
st.set_page_config(page_title="NutriFit Pro: Aplicația Mariei", layout="wide", page_icon="🍎")

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

# 3. INTERFAȚĂ
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
        
        # AICI APAR OPȚIUNILE DE ACTIVITATE CARE LIPSEAU
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
            # Calcul Rata Metabolică Bazală (RMB)
            rmb = (10 * greutate) + (6.25 * 165) - (5 * 30) + (5 if sex == "Masculin" else -161)
            necesar = int(rmb * factor)
            # LOGICA TA: Slabire = Necesar - 1000
            slabire = necesar - 1000
            
            st.session_state.res = {
                "necesar": necesar,
                "slabire": max(slabire, 1200), # Nu coborâm sub 1200 din motive de siguranță
                "p": int((slabire * 0.3) / 4),
                "c": int((slabire * 0.4) / 4),
                "g": int((slabire * 0.3) / 9)
            }
            st.session_state.calculat = True

    with col_out:
        if st.session_state.calculat:
            res = st.session_state.res
            st.subheader("🎯 Rezultate Plan")
            c1, c2 = st.columns(2)
            c1.metric("Calorii Menținere", f"{res['necesar']} kcal")
            c2.metric("Țintă Slăbire (-1000)", f"{res['slabire']} kcal", delta="-1000 kcal")
            
            st.divider()
            fig = px.pie(values=[res['p']*4, res['c']*4, res['g']*9], 
                         names=['Proteine', 'Carbi', 'Grăsimi'],
                         color_discrete_sequence=['#3498db', '#f1c40f', '#e74c3c'], hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("👈 Introdu datele în stânga și apasă pe 'Calculează Planul'.")

# --- TAB 2: MENIU SĂPTĂMÂNAL ---
with tab2:
    if st.session_state.calculat:
        ziua = st.selectbox("Selectează Ziua:", ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"])
        st.subheader(f"🍴 Meniu recomandat pentru {ziua}")
        # Aici poți personaliza meniurile pentru fiecare zi
        st.write("Configurația de macros este salvată. Poți alege alimentele preferate de mai jos.")
        st.info("Sistemul de rotație a alimentelor va fi disponibil în curând.")
    else:
        st.warning("⚠️ Calculează planul mai întâi!")

