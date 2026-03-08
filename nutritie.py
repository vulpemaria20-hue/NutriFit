import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. CONFIGURARE PAGINĂ (OBLIGATORIU PRIMA LINIE)
st.set_page_config(page_title="Aplicația Mariei - NutriFit", layout="wide", page_icon="🍎")

# 2. SISTEM DE SECURITATE (LOGIN)
if "autentificat" not in st.session_state:
    st.session_state.autentificat = False

if not st.session_state.autentificat:
    st.title("🔒 Aplicația Mariei - Acces Restricționat")
    parola_introdusa = st.text_input("Introdu parola de acces:", type="password")
    if st.button("Autentificare"):
        if parola_introdusa == "nutrifit2026":
            st.session_state.autentificat = True
            st.rerun()
        else:
            st.error("Parolă incorectă! Încearcă din nou.")
    st.stop()

# 3. LOGICA DE CALCUL PERSONALIZATĂ
def calculeaza_plan(ga, sex, ic, tip_somatic):
    # Calcul Rată Metabolică Bazală
    rmb = (1 if sex == 'Masculin' else 0.9) * ga * 24
    mentinere = ga * ic
    tinta = max(mentinere * 0.8, rmb)
    
    # Proporții Macros în funcție de Tip Somatic
    ratios = {
        "Ectomorf": [0.25, 0.55, 0.20],
        "Mezomorf": [0.30, 0.40, 0.30], 
        "Endomorf": [0.35, 0.25, 0.40]
    }
    r = ratios[tip_somatic]
    return {
        "rmb": int(rmb), 
        "mentinere": int(mentinere), 
        "tinta": int(tinta),
        "p": round((tinta * r[0]) / 4, 1), 
        "c": round((tinta * r[1]) / 4, 1), 
        "g": round((tinta * r[2]) / 9, 1)
    }

# 4. INTERFAȚĂ PRINCIPALĂ
st.title("🍎 Aplicația Mariei: NutriFit Pro")
st.markdown("---")

if 'calculat' not in st.session_state:
    st.session_state.calculat = False

tab1, tab2, tab3 = st.tabs(["📊 Calculator & Macros", "🍱 Meniuri Personalizate", "📈 Progres"])

# --- TAB 1: CALCULATOR ---
with tab1:
    col_in, col_out = st.columns([1, 2], gap="large")
    with col_in:
        st.subheader("📝 Date Profil")
        nume = st.text_input("Numele tău", "Maria")
        sex = st.radio("Sex", ["Masculin", "Feminin"], index=1, horizontal=True)
        greutate = st.number_input("Greutate actuală (kg)", 40.0, 200.0, 70.0)
        
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
            st.session_state.greutate_initiala = greutate
            st.session_state.calculat = True

    with col_out:
        if st.session_state.calculat:
            res = st.session_state.res
            st.subheader(f"Rezultate pentru {st.session_state.nume}")
            c1, c2, c3 = st.columns(3)
            c1.metric("RMB (Bazal)", f"{res['rmb']} kcal")
            c2.metric("Menținere", f"{res['mentinere']} kcal")
            c3.metric("Țintă Slăbire", f"{res['tinta']} kcal")
            
            st.divider()
            fig = px.pie(values=[res['p']*4, res['c']*4, res['g']*9], 
                         names=['Proteine', 'Carbohidrați', 'Grăsimi'],
                         color_discrete_sequence=['#2ecc71', '#f1c40f', '#e74c3c'], 
                         hole=0.4, title="Distribuție Calorică")
            st.plotly_chart(fig, use_container_width=True)
            st.info(f"👉 **Necesar zilnic:** Proteine: {res['p']}g | Carbohidrați: {res['c']}g | Grăsimi: {res['g']}g")
        else:
            st.info("👈 Maria, introdu datele în stânga pentru a începe.")

# --- TAB 2: MENIURI ---
with tab2:
    if st.session_state.calculat:
        res = st.session_state.res
        st.subheader("🍱 Idei de Mese (Gramaje Calculate)")
        
        surse_p = {"Piept de pui": 23, "Ouă (buc)": 6.5, "Brânză": 15, "Pește": 18, "Iaurt Grecesc": 10}
        surse_c = {"Orez (fiert)": 28, "Cartof": 20, "Ovăz": 60, "Paste": 25, "Quinoa": 21}

        mese = {"🌅 Mic Dejun (25%)": 0.25, "🏙️ Prânz (40%)": 0.40, "🌆 Cină (35%)": 0.35}
        
        for mesa, proc in mese.items():
            with st.expander(mesa, expanded=True):
                c1, c2 = st.columns(2)
                p_necesar = res['p'] * proc
                c_necesar = res['c'] * proc
                
                with c1:
                    s_p = st.selectbox(f"Sursă Proteine", list(surse_p.keys()), key=f"p_{mesa}")
                    gr_p = round((p_necesar / surse_p[s_p]) * 100) if s_p != "Ouă (buc)" else round(p_necesar / 6.5, 1)
                    st.write(f"Necesar: **{gr_p}** {'bucăți' if s_p == 'Ouă (buc)' else 'grame'}")
                with c2:
                    s_c = st.selectbox(f"Sursă Carbohidrați", list(surse_c.keys()), key=f"c_{mesa}")
                    gr_c = round((c_necesar / surse_c[s_c]) * 100)
                    st.write(f"Necesar: **{gr_c} grame**")
    else:
        st.warning("⚠️ Calculează planul în primul tab!")

# --- TAB 3: PROGRES ---
with tab3:
    if st.session_state.calculat:
        st.subheader("📉 Planificare și Export")
        g_tinta = st.number_input("Greutate țintă (kg)", 40.0, 150.0, 65.0)
        dif = abs(st.session_state.greutate_initiala - g_tinta)
        st.success(f"Maria, pentru a slăbi {dif:.1f} kg, ai nevoie de aproximativ {round(dif/0.7)} săptămâni la un ritm sănătos.")
        
        csv_data = pd.DataFrame({
            "Nume": [st.session_state.nume], 
            "Greutate Initiala": [st.session_state.greutate_initiala],
            "Tinta Kcal": [st.session_state.res['tinta']],
            "Proteine(g)": [st.session_state.res['p']]
        }).to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descarcă Planul tău (Excel)", csv_data, "Plan_Maria.csv", "text/csv")
