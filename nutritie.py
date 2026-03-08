import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. CONFIGURARE PAGINĂ
st.set_page_config(page_title="NutriFit Pro", layout="wide")

# 2. LOGICA DE CALCUL
def calculeaza_plan(ga, sex, ic, tip_somatic):
    rmb = (1 if sex == 'Masculin' else 0.9) * ga * 24
    mentinere = ga * ic
    tinta = max(mentinere * 0.8, rmb)
    ratios = {"Ectomorf": [0.25, 0.55, 0.20], "Mezomorf": [0.30, 0.40, 0.30], "Endomorf": [0.35, 0.25, 0.40]}
    r = ratios[tip_somatic]
    return {
        "rmb": int(rmb), "mentinere": int(mentinere), "tinta": int(tinta),
        "p": round((tinta * r[0]) / 4, 1), "c": round((tinta * r[1]) / 4, 1), "g": round((tinta * r[2]) / 9, 1)
    }

# 3. INTERFAȚĂ
st.title("🍎 NutriFit Pro: Consultantul tău Digital")

if 'calculat' not in st.session_state:
    st.session_state.calculat = False

tab1, tab2, tab3 = st.tabs(["📊 Calculator & Macros", "🍱 Meniuri & Alimente Preferate", "📈 Jurnal Progres"])

# --- TAB 1: CALCULATOR ---
with tab1:
    col_in, col_out = st.columns([1, 2], gap="large")
    with col_in:
        st.subheader("📝 Date Profil")
        nume = st.text_input("Nume", "Utilizator")
        sex = st.radio("Sex", ["Masculin", "Feminin"], horizontal=True)
        greutate = st.number_input("Greutate (kg)", 40.0, 200.0, 75.0)
        activitate_optiuni = {
            "Sedentar (Birou)": 30, "Activitate Ușoară": 35, 
            "Moderat Activ": 40, "Foarte Activ": 45, "Performanță": 50
        }
        selectie_activitate = st.selectbox("Nivel de Activitate:", list(activitate_optiuni.keys()))
        ic_ales = activitate_optiuni[selectie_activitate]
        tip = st.selectbox("Tip Somatic:", ["Ectomorf", "Mezomorf", "Endomorf"])
        
        if st.button("CALCULEAZĂ PLANUL"):
            st.session_state.res = calculeaza_plan(greutate, sex, ic_ales, tip)
            st.session_state.nume = nume
            st.session_state.tip = tip
            st.session_state.calculat = True

    with col_out:
        if st.session_state.calculat:
            res = st.session_state.res
            st.subheader(f"Rezultate pentru {st.session_state.nume}")
            c1, c2, c3 = st.columns(3)
            c1.metric("RMB", f"{res['rmb']} kcal")
            c2.metric("Menținere", f"{res['mentinere']} kcal")
            c3.metric("Țintă Slăbire", f"{res['tinta']} kcal")
            st.divider()
            fig = px.pie(values=[res['p']*4, res['c']*4, res['g']*9], names=['Proteine', 'Carbi', 'Grăsimi'],
                         color_discrete_sequence=['#2ecc71', '#f1c40f', '#e74c3c'], hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("👈 Introdu datele în stânga.")

# --- TAB 2: MENIURI & ALIMENTE PREFERATE ---
with tab2:
    if st.session_state.calculat:
        res = st.session_state.res
        st.subheader("🍱 Configurare Meniu Personalizat")
        
        # Secțiunea de adăugat alimente
        with st.expander("➕ Introdu un aliment nou (de pe etichetă)", expanded=False):
            col_a1, col_a2, col_a3 = st.columns(3)
            nume_pref = col_a1.text_input("Nume aliment", "Iaurt Grecesc")
            p_pref = col_a2.number_input("Proteine la 100g", 0.1, 100.0, 10.0)
            c_pref = col_a3.number_input("Carbohidrați la 100g", 0.0, 100.0, 4.0)
            st.info(f"Dacă alegi {nume_pref}, sistemul va recalcula automat gramajul la mesele de mai jos.")

        # Liste de surse
        surse_p = {"Piept de pui": 23, "Ouă (buc)": 6.5, "Brânză": 15, "Pește": 18}
        if nume_pref:
            surse_p[nume_pref] = p_pref
            
        surse_c = {"Orez": 28, "Cartof": 20, "Ovăz": 60, "Paste": 25}

        # Repartizare pe mese
        mese = {"🌅 Mic Dejun (25%)": 0.25, "🏙️ Prânz (40%)": 0.40, "🌆 Cină (35%)": 0.35}
        
        for mesa, proc in mese.items():
            with st.expander(mesa, expanded=True):
                col1, col2 = st.columns(2)
                p_necesar = res['p'] * proc
                c_necesar = res['c'] * proc
                
                with col1:
                    s_p = st.selectbox(f"Sursă Proteine", list(surse_p.keys()), key=f"p_{mesa}")
                    gr_p = round((p_necesar / surse_p[s_p]) * 100) if s_p != "Ouă (buc)" else round(p_necesar / 6.5, 1)
                    st.write(f"👉 **{gr_p}** {'bucăți' if s_p == 'Ouă (buc)' else 'grame'}")
                
                with col2:
                    s_c = st.selectbox(f"Sursă Carbohidrați", list(surse_c.keys()), key=f"c_{mesa}")
                    gr_c = round((c_necesar / surse_c[s_c]) * 100)
                    st.write(f"👉 **{gr_c} grame**")
    else:
        st.warning("⚠️ Calculează planul în primul tab!")

# --- TAB 3: PROGRES ---
with tab3:
    if st.session_state.calculat:
        st.subheader("📉 Jurnal și Export")
        g_tinta = st.number_input("Greutate țintă (kg)", 40.0, 150.0, 70.0)
        st.info(f"Pentru a ajunge de la {greutate}kg la {g_tinta}kg, ai nevoie de aproximativ {round(abs(greutate-g_tinta)/0.7)} săptămâni.")
        
        csv_data = pd.DataFrame({
            "Nume": [st.session_state.nume], "Greutate": [greutate], "Țintă": [g_tinta],
            "Kcal": [st.session_state.res['tinta']], "Proteine": [st.session_state.res['p']]
        }).to_csv(index=False).encode('utf-8')
        
        st.download_button("📥 Descarcă Planul pentru Excel", csv_data, "Plan_Nutritie.csv", "text/csv")
    else:
        st.info("Calculează planul pentru a vedea progresul.")
        import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- 0. SISTEM DE SECURITATE (LOGIN) ---
def verificare_parola():
    if "autentificat" not in st.session_state:
        st.session_state.autentificat = False

    if not st.session_state.autentificat:
        st.title("🔒 Acces Restricționat")
        parola_introdusa = st.text_input("Introdu parola pentru acces:", type="password")
        if st.button("Autentificare"):
            parola_corecta = "nutrifit1968"  # <--- SCHIMBĂ PAROLA AICI
            if parola_introdusa == parola_corecta:
                st.session_state.autentificat = True
                st.rerun()
            else:
                st.error("Parolă incorectă! Contactează administratorul pentru acces.")
        return False
    return True

# --- DACĂ NU E AUTENTIFICAT, OPRIM EXECUȚIA AICI ---
if verificare_parola():

    # --- 1. CONFIGURARE PAGINĂ (Restul codului tău) ---
    st.set_page_config(page_title="NutriFit Pro", layout="wide")
    
    # [Restul codului tău de la pasul anterior începe aici...]
    st.title("🍎 NutriFit Pro: Consultantul tău Digital")
    
    if 'calculat' not in st.session_state:
        st.session_state.calculat = False

    tab1, tab2, tab3 = st.tabs(["📊 Calculator & Macros", "🍱 Meniuri & Alimente Preferate", "📈 Jurnal Progres"])

    # (Aici pui tot restul codului pe care l-am finalizat împreună)
    # ... [Copiaza restul codului din nutritie.py aici sub Tab-uri] ...
    
    # NOTĂ: Asigură-te că indentezi (dai un Tab la dreapta) tot restul codului 

    # pentru a fi în interiorul blocului "if verificare_parola():"
