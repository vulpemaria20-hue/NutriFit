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

# 3. INTERFAȚĂ
st.title("🍎 Aplicația Mariei")

tab1, tab2, tab3 = st.tabs(["📊 Calculator", "🍱 Planificator Săptămânal", "🛒 Listă Cumpărături"])

# --- TAB 1: CALCULATOR ---
with tab1:
    st.subheader("📝 Calculează necesarul tău")
    greutate = st.number_input("Greutate (kg)", 40.0, 200.0, 70.0)
    if st.button("Calculează"):
        necesar = int(10 * greutate + 500) # Formulă simplă de exemplu
        st.success(f"Ținta ta este de {necesar} kcal.")

# --- TAB 2: PLANIFICATOR CU SELECTIE ---
with tab2:
    st.subheader("🍱 Configurează-ți meniul pe 7 zile")
    st.info("Selectează ce dorești să mănânci în fiecare zi. Gustările sunt incluse între mese.")

    zile = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
    
    # Opțiuni pentru mâncare (Poți adăuga/modifica aceste liste)
    optiuni_mic_dejun = ["Omletă cu legume", "Iaurt cu ovăz și fructe", "Pancakes proteice", "Pâine integrală cu avocado"]
    optiuni_gustari = ["O mână de nuci", "Un măr", "Iaurt grecesc", "Baton proteic", "O banană", "Brânză cottage"]
    optiuni_pranz = ["Pui la grătar cu orez", "Pește la cuptor cu sparanghel", "Salată mare cu ton", "Vită cu broccoli"]
    optiuni_cina = ["Supă cremă de linte", "Salată verde cu ou fierte", "Iaurt cu semințe", "Curcan cu salată rucola"]

    # Creăm un dicționar pentru a stoca alegerile
    alegeri = []

    for zi in zile:
        with st.expander(f"📅 Meniu pentru {zi}"):
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                md = st.selectbox(f"Mic Dejun ({zi})", optiuni_mic_dejun)
            with col2:
                g1 = st.selectbox(f"Gustare 1 ({zi})", optiuni_gustari)
            with col3:
                pz = st.selectbox(f"Prânz ({zi})", optiuni_pranz)
            with col4:
                g2 = st.selectbox(f"Gustare 2 ({zi})", optiuni_gustari, index=1)
            with col5:
                cn = st.selectbox(f"Cină ({zi})", optiuni_cina)
            
            alegeri.append({"Zi": zi, "Mic Dejun": md, "Gustare 1": g1, "Prânz": pz, "Gustare 2": g2, "Cină": cn})

    # Afișăm tabelul final recapitulativ
    st.markdown("---")
    st.subheader("📋 Tabelul tău săptămânal")
    df_final = pd.DataFrame(alegeri)
    st.table(df_final)

# --- TAB 3: LISTA ---
with tab3:
    st.subheader("🛒 Lista de Cumpărături")
    st.write("În funcție de selecțiile din Tab-ul 2, asigură-te că ai:")
    st.write("- Ouă, Pui, Pește, Curcan")
    st.write("- Iaurt, Ovăz, Nuci, Fructe")
    st.write("- Legume verzi, Orez, Avocado")
