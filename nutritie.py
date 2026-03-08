import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURARE
st.set_page_config(page_title="Aplicația Mariei", layout="wide")

if "autentificat" not in st.session_state:
    st.session_state.autentificat = False

if not st.session_state.autentificat:
    st.title("🔒 Acces Protejat")
    parola = st.text_input("Parola:", type="password")
    if st.button("Intră"):
        if parola == "nutrifit2026":
            st.session_state.autentificat = True
            st.rerun()
    st.stop()

# 2. LOGICA DE CALCUL (Somatic)
def calculeaza_plan(ga, sex, ic, tip_somatic):
    rmb = (1 if sex == 'Masculin' else 0.9) * ga * 24
    mentinere = ga * ic
    tinta = max(mentinere * 0.8, rmb)
    ratios = {"Ectomorf": [0.25, 0.55, 0.20], "Mezomorf": [0.30, 0.40, 0.30], "Endomorf": [0.35, 0.25, 0.40]}
    r = ratios[tip_somatic]
    return {"tinta": int(tinta), "p": round((tinta * r[0]) / 4, 1), "c": round((tinta * r[1]) / 4, 1), "g": round((tinta * r[2]) / 9, 1)}

st.title("🍎 NutriFit Pro: Aplicația Mariei")

if 'calculat' not in st.session_state:
    st.session_state.calculat = False

tab1, tab2, tab3 = st.tabs(["📊 Calculator", "🍱 Meniu & Cumpărături", "📈 Export"])

with tab1:
    c_in, c_out = st.columns([1, 2])
    with c_in:
        greutate = st.number_input("Greutate (kg)", 40.0, 150.0, 70.0)
        sex = st.radio("Sex", ["Masculin", "Feminin"], index=1)
        tip = st.selectbox("Tip Somatic", ["Ectomorf", "Mezomorf", "Endomorf"])
        if st.button("Generează Plan"):
            st.session_state.res = calculeaza_plan(greutate, sex, 35, tip)
            st.session_state.calculat = True
    
    with c_out:
        if st.session_state.calculat:
            st.success(f"Țintă: {st.session_state.res['tinta']} kcal")
            fig = px.pie(values=[st.session_state.res['p']*4, st.session_state.res['c']*4, st.session_state.res['g']*9], names=['Proteine', 'Carbi', 'Grăsimi'], hole=0.4)
            st.plotly_chart(fig)

with tab2:
    if st.session_state.calculat:
        st.subheader("🛒 Construiește meniul și lista")
        surse_p = {"Piept de pui": 23, "Ouă (buc)": 6.5, "Pește": 18}
        surse_c = {"Orez": 28, "Cartof": 20, "Paste": 25}
        
        lista_cumparaturi = []
        mese = {"Mic Dejun": 0.25, "Prânz": 0.40, "Cină": 0.35}
        
        for mesa, proc in mese.items():
            col1, col2 = st.columns(2)
            with col1:
                s_p = st.selectbox(f"Proteină {mesa}", list(surse_p.keys()), key=f"p_{mesa}")
                gr_p = round((st.session_state.res['p'] * proc / surse_p[s_p]) * 100) if s_p != "Ouă (buc)" else round((st.session_state.res['p'] * proc) / 6.5, 1)
                st.write(f"Cantitate: {gr_p}")
                lista_cumparaturi.append(f"{s_p}: {gr_p} {'buc' if s_p == 'Ouă (buc)' else 'g'}")
            with col2:
                s_c = st.selectbox(f"Carbohidrat {mesa}", list(surse_c.keys()), key=f"c_{mesa}")
                gr_c = round((st.session_state.res['c'] * proc / surse_c[s_c]) * 100)
                st.write(f"Cantitate: {gr_c} g")
                lista_cumparaturi.append(f"{s_c}: {gr_c} g")
        
        st.divider()
        st.subheader("📝 Lista de Cumpărături Finală")
        for item in lista_cumparaturi:
            st.checkbox(item) # Poți bifa produsele direct în aplicație!
    else:
        st.info("Calculează planul mai întâi.")

with tab3:
    if st.session_state.calculat:
        csv = pd.DataFrame({"Aliment": lista_cumparaturi}).to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descarcă Lista de Cumpărături", csv, "Lista_Maria.csv", "text/csv")
