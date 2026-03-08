import streamlit as st
import pandas as pd

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

# 3. INTERFAȚĂ PRINCIPALĂ
st.title("🍎 Aplicația Mariei")

tab1, tab2, tab3 = st.tabs(["📊 Calculator Macros & Obiective", "🍱 Planificator 5 Mese/Zi", "🛒 Listă Cumpărături"])

# --- TAB 1: CALCULATOR COMPLET ---
with tab1:
    st.subheader("📊 Calculează-ți necesarul caloric")
    
    col1, col2 = st.columns(2)
    
    with col1:
        greutate = st.number_input("Greutate actuală (kg):", 40.0, 200.0, 75.0)
        inaltime = st.number_input("Înălțime (cm):", 120, 230, 170)
        varsta = st.number_input("Vârstă:", 15, 90, 30)
        sex = st.radio("Sex:", ["Feminin", "Masculin"], horizontal=True)
    
    with col2:
        activitate_optiuni = {
            "Sedentar (puțin sau deloc exercițiu)": 1.2,
            "Activitate ușoară (1-3 zile/săptămână)": 1.375,
            "Activitate moderată (3-5 zile/săptămână)": 1.55,
            "Foarte activ (6-7 zile/săptămână)": 1.725
        }
        nivel = st.selectbox("Nivel de activitate:", list(activitate_optiuni.keys()))
        factor = activitate_optiuni[nivel]
        
        obiectiv = st.selectbox("Obiectivul tău:", ["Slăbire (-1000 kcal)", "Menținere", "Masă Musculară (+300 kcal)"])

    if st.button("GENEREAZĂ VALORI"):
        # Formula Mifflin-St Jeor
        if sex == "Masculin":
            bmr = (10 * greutate) + (6.25 * inaltime) - (5 * varsta) + 5
        else:
            bmr = (10 * greutate) + (6.25 * inaltime) - (5 * varsta) - 161
            
        mentinere = int(bmr * factor)
        
        if "Slăbire" in obiectiv:
            tinta = mentinere - 1000
        elif "Masă Musculară" in obiectiv:
            tinta = mentinere + 300
        else:
            tinta = mentinere
            
        st.session_state.calculat = True
        st.session_state.tinta = tinta
        st.session_state.mentinere = mentinere

    if st.session_state.get('calculat'):
        st.markdown("---")
        c1, c2 = st.columns(2)
        c1.metric("🔥 Calorii Menținere", f"{st.session_state.mentinere} kcal")
        c2.metric("🎯 ȚINTA TA ZILNICĂ", f"{st.session_state.tinta} kcal", delta=f"{st.session_state.tinta - st.session_state.mentinere} kcal")

# --- TAB 2: PLANIFICATOR 5 MESE ---
with tab2:
    st.subheader("🍱 Meniu Săptămânal (3 Mese + 2 Gustări)")
    
    zile = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
    
    # Opțiuni alimentare
    optiuni_md = ["Omletă", "Ovăz", "Pâine cu avocado", "Iaurt grecesc"]
    optiuni_g = ["Nuci", "Fructe", "Baton proteic", "Brânză cottage", "Semințe"]
    optiuni_p = ["Pui cu orez", "Pește cu legume", "Vită la grătar", "Salată mare cu ton"]
    optiuni_c = ["Supă cremă", "Salată ușoară", "Curcan", "Omletă cu albușuri"]

    alegeri_saptamana = []

    for zi in zile:
        with st.expander(f"📅 Configurează {zi}"):
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1: m_d = st.selectbox(f"Mic Dejun", optiuni_md, key=f"md_{zi}")
            with col2: g_1 = st.selectbox(f"Gustare 1", optiuni_g, key=f"g1_{zi}")
            with col3: p_z = st.selectbox(f"Prânz", optiuni_p, key=f"pz_{zi}")
            with col4: g_2 = st.selectbox(f"Gustare 2", optiuni_g, key=f"g2_{zi}")
            with col5: c_n = st.selectbox(f"Cină", optiuni_c, key=f"cn_{zi}")
            
            alegeri_saptamana.append({
                "Ziua": zi, "Mic Dejun": m_d, "Gustare 1": g_1, 
                "Prânz": p_z, "Gustare 2": g_2, "Cină": c_n
            })

    st.markdown("---")
    st.subheader("📋 Tabel Recapitulativ")
    st.table(pd.DataFrame(alegeri_saptamana))

# --- TAB 3: LISTA ---
with tab3:
    st.subheader("🛒 Necesar Cumpărături")
    st.write("Verifică dacă ai în frigider ingredientele pentru selecțiile făcute în Tab-ul 2.")
